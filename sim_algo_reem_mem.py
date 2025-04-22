#!/usr/bin/env python

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
            ]

def is_valid(virtual_dir, segmentos):
    for i, base, limit in segmentos:
        if base <= virtual_dir < base + limit:
            return True
    return False

def procesar(segmentos, reqs, marcos_libres):
    size_page = 0x10
    table_page = {}
    recent_use = []
    result = []
    
    for req in reqs:
        if not is_valid(req, segmentos):
            result.append((req, 0x1FF, "Segmentation Fault"))
            break

        virtual_page = req // size_page
        offset = req % size_page
        
        if virtual_page in table_page:
            frame = table_page[virtual_page]
            result.append((req, frame * size_page + offset, "Marco ya estaba asignado"))
            recent_use.remove(virtual_page)
            recent_use.append(virtual_page)
        else:
            if marcos_libres:
                frame = marcos_libres.pop(0)
                action = "Marco libre asignado"
            else:
                old_page = recent_use.pop(0)
                frame = table_page.pop(old_page)
                action = "Marco asignado"
            
            table_page[virtual_page] = frame 
            recent_use.append(virtual_page)
            result.append((req, frame * size_page + offset, action))

    return result

def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

