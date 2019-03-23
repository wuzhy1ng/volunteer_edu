# volunteer_edu
大学生志愿家教平台后端开发，采用Django框架，为微信小程序打造

app与路由分配关系：

app：information_service
路由：
    path('register/', views.register),  # 注册信息
    path('register/sms/', views.register_sms),  # 注册验证码
    path('register/safe/', views.register_safe),  # 注册安全模块（暂无）

    path('login/', views.login),  # 登录
    path('logout/', views.logout),  # 登出

    path('home/', views.home),  # 个人中心

    path('update/message/', views.update_message),  # 更新信息
    path('update/image/', views.update_image),  # 更新头像
    path('update/certification/', views.update_certification),  # 更新证书

    path('test/', views.test),  # 测试
   
app：reservation_service
路由：暂无
