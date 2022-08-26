from math import ceil
from main.models import *
from rest_framework.response import Response
from main.api.serilaizers import *
from rest_framework import status
from rest_framework.decorators import api_view
from main.api.services import *

def add_needs_return_list(serial_list, warhou, not_free, needs_dict):
            for i in warhou:
                if i.id in not_free:
                    continue
                for k,v in needs_dict.items():
                    if v==0:
                        continue
                    if i.material_id == k:
                        z = i.remainder - v
                        if z < 0:
                            needs_dict[k] = v- i.remainder
                            create_warehouse_serializer(serial_list, i)

                        elif z == 0:
                            needs_dict[k] = 0
                            create_warehouse_serializer(serial_list, i)
                            not_free.append(i.id)

                        elif z > 0:
                            i.remainder=i.remainder-v
                            create_warehouse_serializer(serial_list, WareHouseModel(part_id=i.part_id, material_id=i.material.id, remainder=v, price=i.price))
                            needs_dict[k] = 0
            return serial_list

@api_view(['POST', 'GET'])
def create_product(request):
    context = {}
    not_free = []
    serial_list = []
    serial_list2 = []

    if request.method == "GET":
        prod = ProductModel.objects.all()
        serializer = ProductSerilizer(prod, many=True)

        return Response(serializer.data)
    else:
        serializer = ResponseMaterialSerializer(data=request.data)
        
        if serializer.is_valid():

            pr_id = serializer.data['product_id']
            count = serializer.data['product_qty']
            pr_id2 = serializer.data['product_id2']
            count2 = serializer.data['product_qty2']


            # berilgan mahsulotni bittasi u.n kerak hom ashyoni chiqarib. bizga k.k miqdorga kopaytiryapman
            try:
                prod = ProductMaterialsModel.objects.filter(name_id=pr_id)
                prod2 = ProductMaterialsModel.objects.filter(name_id=pr_id2)
                prod_name = str(ProductModel.objects.get(id=pr_id))
                prod_name2 = str(ProductModel.objects.get(id=pr_id2))
            except:
                return Response({'status':'wrong data'})

            # ombordan bizga k.k mahsulotlarni partiyasidan qatiynazar chaqiryapman
            warhou = WareHouseModel.objects.all()
            needs_dict = needs_dict_returner(prod,count)
            needs_dict2=needs_dict_returner(prod2, count2)
            serial_list=add_needs_return_list(serial_list, warhou, not_free, needs_dict)
            serial_list2 = add_needs_return_list(serial_list2, warhou, not_free, needs_dict2)

            fix_needs(serial_list, needs_dict)
            fix_needs(serial_list2, needs_dict2)

            base_data = WarehouseSerializer(serial_list, many=True)
            base_data2 = WarehouseSerializer(serial_list2, many=True)

            context['result']=[{'product_name':prod_name, 'product_qty':count, 'product_materials':base_data.data},
            {'product_name':prod_name2, 'product_qty':count2, 'product_materials':base_data2.data}]


            return Response(context)
        else:
            return Response({'status':'wrong data'})