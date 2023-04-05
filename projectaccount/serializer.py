from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Account
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterCustomerSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, read_only=False)
    # password = serializers.CharField(
    #     write_only = True,
    #     required = True,
    #     help_text = 'Enter password',
    #     style = {'input_type': 'password'}
    # )
    
    # confirm password field
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        help_text = 'Enter confirm password',
        style = {'input_type': 'password'}
    )
    # role= serializers.CharField(read_only=True)
    class Meta:
        model=Account
        fields = ['full_name','username','email','phone','password', 'password2']

        read_only_fields = ('password2',)

        extra_kwargs = {
                'password': {'write_only': True},
                
                # 'password2':{'write_only':True}
        }    



        # def save(self):

        #     user = User(
        #         email=self.validated_data['email'],
        #         username=self.validated_data['username'],
        #         phone=self.validated_data['phone'],
        #         full_name=self.validated_data['full_name'],
        #         # password2=self.validated_data('password2')
        #         # role = self.validated_data['role']
                
        #     )
        #     password = self.validated_data['password']

        #     # password2 =self.validated_data.pop('password2')
        #     password2 = self.validated_data['password2']
        #     if password != password2:
        #         raise serializers.ValidationError({'password': 'Passwords must match.'})
        #     user.set_password(password)
        #     user.save()
        #     return user


    def create(self, validated_data):
        
        password = self.validated_data['password']

            # password2 =self.validated_data.pop('password2')
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        else:
            user = Account.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=self.validated_data['full_name'],
                phone=self.validated_data['phone'],
                
                # custom_field=validated_data['custom_field']
            )
            # user.save()

            # password = self.validated_data['password']

            #     # password2 =self.validated_data.pop('password2')
            # password2 = self.validated_data['password2']
            # if password != password2:
            #     raise serializers.ValidationError({'password': 'Passwords must match.'})
            user.set_password(validated_data['password'])
            user.role = 'customer'
            user.save()
            return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.role = 'customer'
    #     if commit:
    #         user.save()
    #     return user

    # def save(self, validated_data):
    #     user=super().save(validated_data)
    #     user.role = 'customer'

        

class RegisterEventTeamSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only = True,
        required = True,
        help_text = 'Enter confirm password',
        style = {'input_type': 'password'}
    )
    
    class Meta:
        model=Account
        fields = ['team_name','username','email','phone','place','work_time','over_view','address','password', 'password2','pin_code']

        read_only_fields = ('password2',)

        extra_kwargs = {
                'password': {'write_only': True},
                
                # 'password2':{'write_only':True}
        }    



    def create(self, validated_data):
        password = self.validated_data['password']

        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        else:
            user = Account.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                team_name=self.validated_data['team_name'],
                phone=self.validated_data['phone'],
                place=self.validated_data['place'],
                work_time=self.validated_data['work_time'],
                over_view=self.validated_data['over_view'],
                address=self.validated_data['address'],
                pin_code=self.validated_data['pin_code'],
                # profile_pic=self.validated_data['profile_pic']
                password=self.validated_data['password']
                


            )
        

            user.set_password(validated_data['password'])
            user.role = 'event_management'
            user.save()
            return user



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (

                   'id',
                   'username',
                   'is_staff',
                   'last_login',
                   'over_view',
                   'work_time',
                   'is_admin',
                   'is_active',
                #    'profile_pic',
                   'full_name',
                   'role',
                   'email', 
                   'is_staff',
                   'address',
                   'phone',
                   'dob',
                   'work_time',
                   'date_joined',
                   'place'

                   
                   )
        
class EventManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (

                    'team_name',
                    'username',
                    'email',
                    'phone',
                    'place',
                    'work_time',
                    'over_view',
                    'address',
                    # 'profile_pic'
                   
                   )
        
