import math


def validate_ip(ip_address: list) -> bool:
    for octet in ip_address:
        if (not octet.isdigit()) or (int(octet) < 0) or (int(octet) > 255):
            return False
    return True


def validate_cidr(cidr: str) -> bool:
    if (cidr == "") or (cidr.isdigit() and 0 <= int(cidr) <= 32):
        return True
    return False


def validate_subnets(num_subnets: str) -> bool:
    if (num_subnets.isdigit()) and (int(num_subnets) > 0):
        return True
    else:
        return False


def mask(ip_address: list, cidr: str):
    if cidr == "":
        if (1 <= ip_address[0]) <= 127:
            mask_ip = [255, 0, 0, 0]
            cidr = "8"
        elif 128 <= ip_address[0] <= 191:
            mask_ip = [255, 255, 0, 0]
            cidr = "16"
        elif 192 <= ip_address[0] <= 223:
            mask_ip = [255, 255, 255, 0]
            cidr = "24"
    else:
        mask_ip = [0, 0, 0, 0]
        for i in range(int(cidr)):
            mask_ip[i // 8] += (1 << (7 - i % 8))
    return mask_ip, cidr


def network(mask_ip: list, ip: list) -> list:
    # Get 2 lists 
    # AND operation between mask address and ip address
    network_ip = []
    for i in range(4):
        network_ip.append(mask_ip[i] & ip[i])
    return network_ip


def reverse(mask: list) -> list:
    # get list
    # reversed = ~ mask & 0xFF
    reversed_mask = []
    for i in range(4):
        reversed_mask.append(~mask[i] & 0xFF)
    return reversed_mask


def broadcast(mask: list, network: list) -> list:
    # Network address OR reversed_mask
    reversed_mask = reverse(mask)
    broadcast_ip = []
    for i in range(4):
        broadcast_ip.append(reversed_mask[i] | network[i])
    return broadcast_ip


def first_addr(broadcast_ip: list, network_ip: list) -> list:
    first_addr_ip = []
    for i in range(4):
        if broadcast_ip[i] == network_ip[i]:
            first_addr_ip.append(network_ip[i])
        else:
            # broadcast_ip[i] = ~ broadcast_ip[i] & 0xFF
            if i == 3:
                first_addr_ip.append((network_ip[i] + 1))
            else:
                first_addr_ip.append(network_ip[i])
    return first_addr_ip


def last_addr(broadcast_ip: list) -> list:
    last_addr_ip = broadcast_ip.copy()
    last_addr_ip[-1] = last_addr_ip[-1] & 0xFE
    return last_addr_ip


def num_hosts(cidr: str) -> int:
    return 2 ** (32 - int(cidr)) - 2


def calc_subnets_cidr(hosts: int, subnets_num: int) -> int:
    hosts_per_subnets = hosts // subnets_num
    subnets_cidr = 32 - int(math.log(hosts_per_subnets, 2))
    return subnets_cidr
