import tkinter as tk
from tkinter import messagebox
from functions import *


def entries_update(octets: list, ip_add: list):
    for i in range(4):
        octets[i].configure(state=tk.NORMAL)
        octets[i].insert(tk.END, str(ip_add[i]))
        octets[i].configure(state=tk.DISABLED)


def submit():
    ip_address = [first_value.get(), second_value.get(), third_value.get(), fourth_value.get()]

    if (validate_ip(ip_address)) and (validate_cidr(cidr_value.get())):

        ip_address_int = [int(octet) for octet in ip_address]
        subnet_mask, cidr_new = mask(ip_address_int, cidr_value.get())
        cidr_value.set(cidr_new)
        entries_update(subnet_mask_octets, subnet_mask)

        network_add = network(subnet_mask, ip_address_int)
        entries_update(network_octets, network_add)

        broadcast_ip = broadcast(subnet_mask, network_add)
        entries_update(broadcast_octets, broadcast_ip)

        first_host_ip = first_addr(broadcast_ip, network_add)
        entries_update(first_host_octets, first_host_ip)

        last_host_ip = last_addr(broadcast_ip)
        entries_update(last_host_octets, last_host_ip)

        next_subnet_ip = next_subnet(broadcast_ip)
        entries_update(next_octets, next_subnet_ip)

        hosts = num_hosts(cidr_value.get())
        hosts_entry.configure(state=tk.NORMAL)
        hosts_value.set(str(hosts))
        hosts_entry.configure(state=tk.DISABLED)

    else:
        messagebox.showerror('Error', 'field must contain numbers 0-255')
        clear()


def calc_subnets():
    if validate_subnets(subnets_value.get()):
        number_of_hosts = int(hosts_value.get())
        number_of_subnets = int(subnets_value.get())
        if number_of_hosts // number_of_subnets >= 4:
            subnets_cidr = calc_subnets_cidr(number_of_hosts, number_of_subnets)
            subnets_CIDR_entry.configure(state=tk.NORMAL)
            subnets_CIDR_value.set(str(subnets_cidr))
            subnets_CIDR_entry.configure(state=tk.DISABLED)
        else:
            messagebox.showerror('Error', 'Subnets number is too high')
            add_subnets_entry.delete(0, tk.END)
    else:
        messagebox.showerror('Error', 'Enter a valid Number')
        add_subnets_entry.delete(0, tk.END)


def delete_entries(entries: list):
    for entry in entries:
        entry.configure(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.configure(state=tk.DISABLED)


def clear():
    delete_entries(target_ip_octets)
    for octet_ip in target_ip_octets:
        octet_ip.configure(state=tk.NORMAL)
    delete_entries(subnet_mask_octets)
    delete_entries(network_octets)
    delete_entries(first_host_octets)
    delete_entries(last_host_octets)
    delete_entries(broadcast_octets)
    delete_entries(next_octets)
    delete_entries([add_subnets_entry, subnets_CIDR_entry, hosts_entry])


def enable_subnets():
    if x.get() == 1:
        add_subnets_entry.configure(state=tk.NORMAL)
    else:
        add_subnets_entry.configure(state=tk.DISABLED)


window = tk.Tk()
window.geometry("1200x600")
window.title("Subnet Calculator")
window.config(background="#d7d7d9")
main_label = tk.Label(window,
                      text="\nIPv4 Subnetting Calculator:\n",
                      font=('Arial', 20, 'bold'),
                      bg="#d7d7d9")
main_label.grid(row=0, column=0, columnspan=3)

# ----------------------------------------TARGET_IP_ADDRESS

target_ip_address = tk.Label(window,
                             text="\nTarget IP Address\n",
                             font=('Arial', 15, 'bold'),
                             bg="#d7d7d9")
target_ip_address.grid(row=1, column=0)

space = tk.Label(window,
                 text="    ",
                 font=('Arial', 10, 'bold'),
                 bg="#d7d7d9")
space.grid(row=1, column=1)

first_value = tk.StringVar()
first_octet = tk.Entry(window,
                       font=('Arial', 10, 'bold'),
                       textvariable=first_value,
                       width=10)
first_octet.grid(row=1, column=2)

dot_1 = tk.Label(window,
                 text="  .  ",
                 font=('Arial', 10, 'bold'),
                 bg="#d7d7d9")
dot_1.grid(row=1, column=3)

second_value = tk.StringVar()
second_octet = tk.Entry(window,
                        font=('Arial', 10, 'bold'),
                        textvariable=second_value,
                        width=10)
second_octet.grid(row=1, column=4)

dot_2 = tk.Label(window,
                 text="  .  ",
                 font=('Arial', 10, 'bold'),
                 bg="#d7d7d9")
dot_2.grid(row=1, column=5)

third_value = tk.StringVar()
third_octet = tk.Entry(window,
                       font=('Arial', 10, 'bold'),
                       textvariable=third_value,
                       width=10)
third_octet.grid(row=1, column=6)

dot_3 = tk.Label(window,
                 text="  .  ",
                 font=('Arial', 10, 'bold'),
                 bg="#d7d7d9")
dot_3.grid(row=1, column=7)

fourth_value = tk.StringVar()
fourth_octet = tk.Entry(window,
                        font=('Arial', 10, 'bold'),
                        textvariable=fourth_value,
                        width=10)
fourth_octet.grid(row=1, column=8)

slash = tk.Label(window,
                 text="  /  ",
                 font=('Arial', 10, 'bold'),
                 bg="#d7d7d9")
slash.grid(row=1, column=9)

cidr_value = tk.StringVar()
cidr_entry = tk.Entry(window,
                      font=('Arial', 10, 'bold'),
                      textvariable=cidr_value,
                      width=5)
cidr_entry.grid(row=1, column=10)

target_ip_octets = [first_octet, second_octet, third_octet, fourth_octet, cidr_entry]

space_2 = tk.Label(window,
                   text="    ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
space_2.grid(row=1, column=11)

submit_button = tk.Button(window,
                          text="Submit",
                          font=('Arial', 10, 'bold'),
                          width=15,
                          cursor="hand2",
                          command=submit)
submit_button.grid(row=1, column=12)

space_3 = tk.Label(window,
                   text="    ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
space_3.grid(row=1, column=13)

clear_button = tk.Button(window,
                         text="Clear",
                         font=('Arial', 10, 'bold'),
                         width=15,
                         cursor="hand2",
                         command=clear)
clear_button.grid(row=1, column=14)

# ----------------------------------------SUBNET-MASK

subnet_title = tk.Label(window,
                        text="\nSubnet-Mask\n",
                        font=('Arial', 10, 'bold'),
                        bg="#d7d7d9")
subnet_title.grid(row=2, column=0)

first_octet_sm = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
first_octet_sm.grid(row=2, column=2)

dot_1_sm = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_1_sm.grid(row=2, column=3)

second_octet_sm = tk.Entry(window,
                           font=('Arial', 10, 'bold'),
                           state=tk.DISABLED,
                           width=10)
second_octet_sm.grid(row=2, column=4)

dot_2_sm = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_2_sm.grid(row=2, column=5)

third_octet_sm = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
third_octet_sm.grid(row=2, column=6)

dot_3_sm = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_3_sm.grid(row=2, column=7)

fourth_octet_sm = tk.Entry(window,
                           font=('Arial', 10, 'bold'),
                           state=tk.DISABLED,
                           width=10)
fourth_octet_sm.grid(row=2, column=8)

subnet_mask_octets = [first_octet_sm, second_octet_sm, third_octet_sm, fourth_octet_sm]

# ----------------------------------------NETWORK

network_title = tk.Label(window,
                         text="\nNetwork\n",
                         font=('Arial', 10, 'bold'),
                         bg="#d7d7d9")
network_title.grid(row=3, column=0)

first_octet_n = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
first_octet_n.grid(row=3, column=2)

dot_1_n = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_1_n.grid(row=3, column=3)

second_octet_n = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
second_octet_n.grid(row=3, column=4)

dot_2_n = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_2_n.grid(row=3, column=5)

third_octet_n = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
third_octet_n.grid(row=3, column=6)

dot_3_n = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_3_n.grid(row=3, column=7)

fourth_octet_n = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
fourth_octet_n.grid(row=3, column=8)

network_octets = [first_octet_n, second_octet_n, third_octet_n, fourth_octet_n]

# ----------------------------------------FIRST_HOST

first_host = tk.Label(window,
                      text="\nFirst Host\n",
                      font=('Arial', 10, 'bold'),
                      bg="#d7d7d9")
first_host.grid(row=4, column=0)

first_octet_f = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
first_octet_f.grid(row=4, column=2)

dot_1_f = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_1_f.grid(row=4, column=3)

second_octet_f = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
second_octet_f.grid(row=4, column=4)

dot_2_f = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_2_f.grid(row=4, column=5)

third_octet_f = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
third_octet_f.grid(row=4, column=6)

dot_3_f = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_3_f.grid(row=4, column=7)

fourth_octet_f = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
fourth_octet_f.grid(row=4, column=8)

first_host_octets = [first_octet_f, second_octet_f, third_octet_f, fourth_octet_f]

# ----------------------------------------LAST_HOST

last_host = tk.Label(window,
                     text="\nLast Host\n",
                     font=('Arial', 10, 'bold'),
                     bg="#d7d7d9")
last_host.grid(row=5, column=0)

first_octet_l = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
first_octet_l.grid(row=5, column=2)

dot_1_l = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_1_l.grid(row=5, column=3)

second_octet_l = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
second_octet_l.grid(row=5, column=4)

dot_2_l = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_2_l.grid(row=5, column=5)

third_octet_l = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
third_octet_l.grid(row=5, column=6)

dot_3_l = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_3_l.grid(row=5, column=7)

fourth_octet_l = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
fourth_octet_l.grid(row=5, column=8)

last_host_octets = [first_octet_l, second_octet_l, third_octet_l, fourth_octet_l]

# ----------------------------------------BROADCAST

broadcast_title = tk.Label(window,
                           text="\nBroadcast\n",
                           font=('Arial', 10, 'bold'),
                           bg="#d7d7d9")
broadcast_title.grid(row=6, column=0)

first_octet_b = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
first_octet_b.grid(row=6, column=2)

dot_1_b = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_1_b.grid(row=6, column=3)

second_octet_b = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
second_octet_b.grid(row=6, column=4)

dot_2_b = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_2_b.grid(row=6, column=5)

third_octet_b = tk.Entry(window,
                         font=('Arial', 10, 'bold'),
                         state=tk.DISABLED,
                         width=10)
third_octet_b.grid(row=6, column=6)

dot_3_b = tk.Label(window,
                   text="  .  ",
                   font=('Arial', 10, 'bold'),
                   bg="#d7d7d9")
dot_3_b.grid(row=6, column=7)

fourth_octet_b = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
fourth_octet_b.grid(row=6, column=8)

broadcast_octets = [first_octet_b, second_octet_b, third_octet_b, fourth_octet_b]

# ----------------------------------------NEXT_SUBNET

next_subnet_title = tk.Label(window,
                             text="\nNext Subnet\n",
                             font=('Arial', 10, 'bold'),
                             bg="#d7d7d9")
next_subnet_title.grid(row=7, column=0)

first_octet_ns = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
first_octet_ns.grid(row=7, column=2)

dot_1_ns = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_1_ns.grid(row=7, column=3)

second_octet_ns = tk.Entry(window,
                           font=('Arial', 10, 'bold'),
                           state=tk.DISABLED,
                           width=10)
second_octet_ns.grid(row=7, column=4)

dot_2_ns = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_2_ns.grid(row=7, column=5)

third_octet_ns = tk.Entry(window,
                          font=('Arial', 10, 'bold'),
                          state=tk.DISABLED,
                          width=10)
third_octet_ns.grid(row=7, column=6)

dot_3_ns = tk.Label(window,
                    text="  .  ",
                    font=('Arial', 10, 'bold'),
                    bg="#d7d7d9")
dot_3_ns.grid(row=7, column=7)

fourth_octet_ns = tk.Entry(window,
                           font=('Arial', 10, 'bold'),
                           state=tk.DISABLED,
                           width=10)
fourth_octet_ns.grid(row=7, column=8)

next_octets = [first_octet_ns, second_octet_ns, third_octet_ns, fourth_octet_ns]

# ----------------------------------------HOSTS
hosts_value = tk.StringVar()
hosts_title = tk.Label(window,
                       text="\nNum of Hosts\n",
                       font=('Arial', 10, 'bold'),
                       bg="#d7d7d9")
hosts_title.grid(row=2, column=12)

hosts_entry = tk.Entry(window,
                       font=('Arial', 10, 'bold'),
                       width=15,
                       state=tk.DISABLED,
                       textvariable=hosts_value)
hosts_entry.grid(row=2, column=14)

# ----------------------------------------CALC_SUBNETS

x = tk.IntVar()
check_button = tk.Checkbutton(window,
                              text="Add Subnets",
                              font=('Arial', 10, 'bold'),
                              bg="#d7d7d9",
                              variable=x,
                              onvalue=1,
                              offvalue=0,
                              command=enable_subnets)
check_button.grid(row=3, column=12)

add_subnets_title = tk.Label(window,
                             text="\nNum of Subnets\n",
                             font=('Arial', 10, 'bold'),
                             bg="#d7d7d9")
add_subnets_title.grid(row=4, column=12)

subnets_value = tk.StringVar()
add_subnets_entry = tk.Entry(window,
                             font=('Arial', 10, 'bold'),
                             state=tk.DISABLED,
                             width=15,
                             textvariable=subnets_value)
add_subnets_entry.grid(row=4, column=14)

calc_button = tk.Button(window,
                        text="Calc CIDR",
                        font=('Arial', 10, 'bold'),
                        width=15,
                        cursor="hand2",
                        command=calc_subnets)
calc_button.grid(row=5, column=12)

subnets_CIDR_value = tk.StringVar()
subnets_CIDR_entry = tk.Entry(window,
                              font=('Arial', 10, 'bold'),
                              state=tk.DISABLED,
                              width=15,
                              textvariable=subnets_CIDR_value)
subnets_CIDR_entry.grid(row=5, column=14)

window.mainloop()