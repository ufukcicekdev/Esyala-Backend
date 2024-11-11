from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from customerauth.models import RoomType, HomeType, HomeModel, SpaceDefinition, TimeRange, MyStyles, User
from customerauth.MyStyleProcess.mystyleserializers import *
from products.models import Product
from main.serializers import *
from rest_framework.pagination import PageNumberPagination

class RoomTypeSelectionAPIView(APIView):
    permission_classes = [IsAuthenticated] #TODO:düzelticek
    serializer_class = RoomTypeListSerializer()
    def get(self, request):
        active_room_types = RoomType.objects.filter(is_active=True)
        serializer = RoomTypeListSerializer(active_room_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        selected_room_type_id must be sent in the body
        """
        serializer = RoomTypePostSerializer(data=request.data)
        if serializer.is_valid():
            selected_room_type_id = request.data.get('selected_room_type_id')
            user = request.user

            try:
                mystyles = MyStyles.objects.get(user=user)
                if selected_room_type_id:
                    mystyles.room_type_id = selected_room_type_id
                    mystyles.save()
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Güncellendi!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
            except MyStyles.DoesNotExist:
                if selected_room_type_id:
                    MyStyles.objects.create(user=user, room_type_id=selected_room_type_id)
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Eklendi!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HomeTypeSelectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeTypeListSerializer()
    def get(self, request):
        active_home_types = HomeType.objects.filter(is_active=True)
        serializer = HomeTypeListSerializer(active_home_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        selected_home_type_id must be sent in the body
        """
        serializer = HomeTypePostSerializer(data=request.data)
        if serializer.is_valid():
            selected_home_type_id = request.data.get('selected_home_type_id')
            user = request.user
            
            try:
                mystyles = MyStyles.objects.get(user=user)
                if selected_home_type_id:
                    mystyles.home_type_id = selected_home_type_id
                    mystyles.save()
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Güncellendi!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
            except MyStyles.DoesNotExist:
                if selected_home_type_id:
                    MyStyles.objects.create(user=user, home_type_id=selected_home_type_id)
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Eklendi!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeModelSelectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeModelListSerializer()
    def get(self, request):
        active_home_types = HomeModel.objects.filter(is_active=True)
        serializer = HomeModelListSerializer(active_home_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        selected_home_model_id must be sent in the body
        """
        serializer = HomeModelPostSerializer(data=request.data)
        if serializer.is_valid():
            selected_home_model_id = request.data.get('selected_home_model_id')
            user = request.user
            
            try:
                mystyles = MyStyles.objects.get(user=user)
                if selected_home_model_id:
                    mystyles.home_model_id = selected_home_model_id
                    mystyles.save()
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Güncellendi!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
            except MyStyles.DoesNotExist:
                if selected_home_model_id:
                    MyStyles.objects.create(user=user, home_model_id=selected_home_model_id)
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Eklendi!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpaceDefinitionSelectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpaceDefinitionListSerializer()
    def get(self, request):
        active_home_types = SpaceDefinition.objects.filter(is_active=True)
        serializer = SpaceDefinitionListSerializer(active_home_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        selected_space_def_id must be sent in the body
        """
        serializer = SpaceDefinitionPostSerializer(data=request.data)
        if serializer.is_valid():
            selected_space_def_id = request.data.get('selected_space_def_id')
            user = request.user
            
            try:
                mystyles = MyStyles.objects.get(user=user)
                if selected_space_def_id:
                    mystyles.space_definition_id = selected_space_def_id
                    mystyles.save()
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Güncellendi!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
            except MyStyles.DoesNotExist:
                if selected_space_def_id:
                    MyStyles.objects.create(user=user, space_definition_id=selected_space_def_id)
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Eklendi!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeRangeSelectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeRangeListSerializer()
    def get(self, request):
        active_home_types = TimeRange.objects.filter(is_active=True)
        serializer = TimeRangeListSerializer(active_home_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        selected_time_range_id must be sent in the body
        """
        serializer = TimeRangePostSerializer(data=request.data)
        if serializer.is_valid():
            selected_time_range_id = request.data.get('selected_time_range_id')
            user = request.user
            
            try:
                mystyles = MyStyles.objects.get(user=user)
                if selected_time_range_id:
                    mystyles.time_range_id = selected_time_range_id
                    mystyles.save()
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Güncellendi!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
            except MyStyles.DoesNotExist:
                if selected_time_range_id:
                    MyStyles.objects.create(user=user, time_range_id=selected_time_range_id)
                    update_user_my_style_status(user)
                    return Response({'status': 'success', 'message': 'Başarıyla Eklendi!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'error', 'message': 'Geçersiz Bir Model Seçildi!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





def update_user_my_style_status(user):
    mystyles_exists = MyStyles.objects.filter(user=user).exists()
    if mystyles_exists:
        mystyles = MyStyles.objects.get(user=user)

        if mystyles.room_type and mystyles.home_type and mystyles.home_model and mystyles.space_definition and mystyles.time_range:
            User.objects.filter(pk=user.pk).update(my_style=True)



class MyStyleListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializers 
    def get(self, request):
        user = request.user

        try:
            my_styles = MyStyles.objects.get(user=get_object_or_404(User, id=6))  #TODO: düzeltilecek

            filtered_products = set()

            if my_styles.room_type:
                room_type_products = Product.objects.filter(room_types=my_styles.room_type, is_active=True)
                filtered_products.update(room_type_products)

            if my_styles.home_type:
                home_type_products = Product.objects.filter(home_types=my_styles.home_type, is_active=True)
                filtered_products.update(home_type_products)

            if my_styles.home_model:
                home_model_products = Product.objects.filter(home_models=my_styles.home_model, is_active=True)
                filtered_products.update(home_model_products)

            if my_styles.space_definition:
                space_definition_products = Product.objects.filter(space_definitions=my_styles.space_definition, is_active=True)
                filtered_products.update(space_definition_products)

            if my_styles.time_range:
                time_range_products = Product.objects.filter(time_ranges=my_styles.time_range, is_active=True)
                filtered_products.update(time_range_products)

            products = list(filtered_products)

            # Paginator ayarları
            # paginator = PageNumberPagination()
            # paginated_products = paginator.paginate_queryset(products, request)

            # Serializer ile ürünleri dönüştür
            serializer = CategoryProductSerializers(products, many=True)

            product_count = len(products)

            return Response({
                'products': serializer.data,
                'product_count': product_count,
            })

        except MyStyles.DoesNotExist:
            return Response({'products': [], 'product_count': 0})
        


class MyStyleCategoryListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MyStyleCategoryListSerializer 
    def get(self, request):
        try:
            user = get_object_or_404(User, id=6)  # TODO: Kullanıcı dinamik olarak alınmalı
            my_styles = MyStyles.objects.get(user=user)

            serializer = MyStyleCategoryListSerializer(my_styles)
            return Response(serializer.data)

        except MyStyles.DoesNotExist:
            return Response({
                'room_type_data': [],
                'home_type_data': [],
                'home_model_data': [],
                'space_definition_data': [],
                'time_range_data': [],
            }, status=404)
        

class MyStyleCategoryProductListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializers 
    def get(self, request):
        """
        http://127.0.0.1:8000/customerauth/user/mystyle-category-product-list/?room_type=3
        Example => ?room_type=1
        room_type = 1
        home_type = 1
        home_model =1
        space_definition = 1
        time_range = 1
        """


        filtered_products = Product.objects.filter(is_active=True)

        room_type = request.query_params.get('room_type')
        home_type = request.query_params.get('home_type')
        home_model = request.query_params.get('home_model')
        space_definition = request.query_params.get('space_definition')
        time_range = request.query_params.get('time_range')

        if room_type:
            filtered_products = filtered_products.filter(room_types__id=room_type)

        if home_type:
            filtered_products = filtered_products.filter(home_types__id=home_type)

        if home_model:
            filtered_products = filtered_products.filter(home_models__id=home_model)

        if space_definition:
            filtered_products = filtered_products.filter(space_definitions__id=space_definition)

        if time_range:
            filtered_products = filtered_products.filter(time_ranges__id=time_range)

        serializer = CategoryProductSerializers(filtered_products, many=True)
        
        return Response({'products': serializer.data, 'product_count': filtered_products.count()})