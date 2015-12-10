import library as lib
import hosts
import pprint

# Devices that all VPCs/Subnets may potentially have and Subnet number (must fit under SUBNET_CIDR)
# Subnet number can be a single number or a list of numbers
ADDRESSES = {
    "web": range(10, 20),
    "db": range(20, 30),
}


DEVICES = ["inet_gw", "web", "vpc_peering"]

# vpc_peering adds a route to the internal route table
# need to add a route to the external route table
ROUTE = {"ExternalPeerRoute" : {"Type" : "AWS::EC2::Route",
                                "Properties" : {
                                    "RouteTableId" : { "Ref" : "ExternalRouteTable" },
                                    "DestinationCidrBlock" : { "Ref" : "PeerVPCSubnet" },
                                    "VpcPeeringConnectionId" : { "Ref" : "VPCPeer" }
                                }}}

def verify_domain(domain):
    if len(domain.split(".")) != 3: # subnet.vpc.tld
        raise Exception("Not a valiid Subnet domain name")

def generate(folder, domain):
    verify_domain(domain)
    
    parameters, resources = lib.load_devices(*DEVICES)
    template = lib.create_template(parameters, resources)
    
    lib.save_template(template, folder, "production." + domain)

def create(session, domain):
    verify_domain(domain)
    
    vpc_domain = domain.split(".", 1)[1]
    vpc_id = lib.vpc_id_lookup(session, vpc_domain)
    
    args = [
        lib.template_argument("KeyName",              lib.keypair_lookup(session)),
        lib.template_argument("VPCId",                vpc_id),
        lib.template_argument("SubnetId",             lib.subnet_id_lookup(session, domain)),
        lib.template_argument("PeerVPCId",            lib.vpc_id_lookup(session, "core.boss")),
        lib.template_argument("PeerVPCSubnet",        hosts.lookup("core.boss")),
        lib.template_argument("InternalRouteTable",   lib.rt_lookup(session, vpc_id, "internal")),
        lib.template_argument("DefaultSecurityGroup", lib.sg_lookup(session, vpc_id, "default")),
        lib.template_argument("WebAMI",               lib.ami_lookup(session, "web.boss")),
        lib.template_argument("WebHostname",          "web." + domain),
        lib.template_argument("WebIP",                hosts.lookup("web." + domain, ADDRESSES)),
    ]
    
    token = lib.generate_token()
    
    parameters, resources = lib.load_devices(*DEVICES)
    resources.update(ROUTE)
    lib.add_userdata(resources, "WebServerInstance", token)
    template = lib.create_template(parameters, resources)
    stack_name = lib.domain_to_stackname("production." + domain)
    
    lib.cloudformation_create(session, stack_name, template, args)
    
    lib.peer_route_update(session, vpc_domain, "core.boss")