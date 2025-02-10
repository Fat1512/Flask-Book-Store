## Introduction
This is a web application built using Flask with the Model-View-Controller (MVC) architecture. The website provides an intuitive shopping experience, secure payment processing, and an admin panel for managing books and orders, and revenue,... The project is deployed on docker with Nginx as proxy server acting as load balancer to ensure the HA !
## Features
- Basic user authentication
- Shopping cart
- Online order payment processing with VNPay
- In-person transaction with QR code scanning
- Admin Panel for tracking revenue, books, orders, inventory, users...
- Search capability is powered by Elastic Search with Debezium as data synchronization
- SMS notification with SendGrid
- Image uploading with Cloudinary
## Installation
Docker installation is required ! Please pay attention to environment variables.
Execute the below to run project !
```sh
docker compose up
```
## Additional Information
Mock VNPay Payment Information
```
Ngân hàng: NCB
Số thẻ: 9704198526191432198
Tên chủ thẻ: NGUYEN VAN A
Ngày phát hành: 07/15
Mật khẩu OTP: 123456
```
## Contributors
- **[Le Tan Phat](https://github.com/Fat1512)**
- **[Le Tan](https://github.com/tanle9t2)**
- **[Trinh Gia Phuc](https://github.com/trinhgiaphuc24)**
