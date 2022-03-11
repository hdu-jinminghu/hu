"""Prun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .backend.api import api 

api_urlpatterns = [
    path('init', api.get_all_file),  #! 文件
    path('structure', api.get_graph), #!  模型结构
    path('rControl', api.r_control),  #! 读取控制参数
    path('cControl', api.c_control),  #! 修改控制参数
    path('rank', api.get_rank),  #!  relu层秩
    path('sensitivity', api.get_sensitivity),  #!  卷积核敏感度
    path('scalar', api.get_scalar),  #!  精确度和损失值
    path('parameters', api.parameters),  #!  模型大小
    path('weight', api.get_weight),  #!  权重
    path('weightGrad', api.get_weight_grad),  #!  权重梯度
    path('bias', api.get_bias),  #!  偏置 
    path('biasGrad', api.get_bias_grad),  #!  偏置梯度
    path('monitor',api.set_monitor),  #! 设置监听节点列表
    path('cycle',api.set_cycle),     #!  设置循环
    path('tempData',api.set_node_),  #!  实时访问时保存临时数据
    path('prun',api.set_prun),  #!  剪枝通道
    path('palyTag',api.set_playTag),  #!  模型运行
    path('batchsize',api.set_batchsize),  #!  批大小
    path('dropout',api.set_dropout),  #!  dropout
    path('trainCycle',api.set_trainCycle),  #!  迭代次数
    path('lr',api.set_lr),  #!  学习率
    path('keep',api.set_keep),  #!  学习率
    path('trainData',api.get_traindata),    #!   训练历史
    path('modelTxt',api.modelTxt),    #!   训练历史
    path('testData', api.get_test),  #! 文件
    path('automlList', api.get_automl_list),  #! automl数据
    path('automlGraph', api.get_automl_graph),  #! 模型结构
    path('automlProcess', api.exec_automl),  #! 执行automl
    path('rough', api.exec_roughautoml),  #!
    path('graph',api.exec_graphUrlDealer) #! 模型结构数据
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path(r'', TemplateView.as_view(template_name='index.html'))
]
