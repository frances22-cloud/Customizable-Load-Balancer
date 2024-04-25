import math

class ConsistentHash:
    def __init__(self, n_servers=3, n_slots=512, n_virtual_servers=9):
        self.n_servers = n_servers
        self.n_slots = n_slots
        self.n_virtual_servers = n_virtual_servers
        self.hash_map = [None] * n_slots

        # Map server containers to slots using virtual servers
        for server_id in range(n_servers):
            for virt_server_id in range(n_virtual_servers):
                slot = self.phi(server_id, virt_server_id)
                self.hash_map[slot] = server_id

    def h(self, request_id):
        return (request_id + (2 * request_id ** 2) + 17) % self.n_slots

    def phi(self, server_id, virt_server_id):
        return (server_id + virt_server_id + (2 * virt_server_id ** 2) + 25) % self.n_slots

    def get_server(self, request_id):
        slot = self.h(request_id)
        server_id = self.hash_map[slot]

        if server_id is None:
            # Apply linear probing
            offset = 1
            while True:
                next_slot = (slot + offset) % self.n_slots
                server_id = self.hash_map[next_slot]
                if server_id is not None:
                    break
                offset += 1

        return server_id