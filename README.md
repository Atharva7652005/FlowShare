# FlowShare

FlowShare is a cloud-enabled collaboration platform designed for secure file sharing and real-time communication. The system allows users to create storage rooms, manage files, and collaborate through integrated video meetings while leveraging AWS cloud services for scalability, storage, load balancing, and deployment.

---

# Features

- Secure user authentication and authorization
- Room-based file sharing system
- Upload, download, update, and delete files
- Real-time video meeting functionality
- Cloud-based scalable architecture
- Persistent file availability
- Load-balanced application deployment
- Fast and responsive user experience
- Secure and reliable cloud infrastructure

---

# AWS Services Used

| Service | Purpose |
|----------|----------|
| AWS EC2 | Application hosting |
| AWS S3 | Cloud file storage |
| AWS RDS (PostgreSQL) | Relational database management |
| AWS Elastic Load Balancer (ELB) | Traffic distribution and scalability |
| AWS ElastiCache (Redis) | Caching and session management |
| AWS IAM | Access and permission management |

---

# Technology Stack

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Django
- Django REST Framework

## Database
- PostgreSQL

## Cloud & DevOps
- AWS EC2
- AWS S3
- AWS RDS
- AWS Elastic Load Balancer
- AWS ElastiCache (Redis)
- Nginx

## Real-Time Communication
- WebRTC
- WebSockets

---

# System Modules

## Authentication Module
- User registration
- Secure login
- Session handling
- Role-based access control

## Storage Management Module
- Create storage rooms
- Upload and manage files
- Secure cloud storage access

## Meeting Module
- Create meeting rooms
- Join meetings using Room ID
- Real-time audio/video communication

## Admin Module
- Manage users
- Monitor storage usage
- Manage system resources

---

# System Architecture

```text
                    Client Browser
                           │
                           ▼
                 AWS Load Balancer (ELB)
                           │
                           ▼
                        Nginx
                           │
                           ▼
                  Django Backend API
                    │            │
         ┌──────────┘            └──────────┐
         ▼                                  ▼
   AWS ElastiCache                    AWS RDS
       (Redis)                     (PostgreSQL)
         │
         ▼
      AWS S3
  (File Storage)

         │
         ▼
WebRTC + WebSocket Server
(Real-Time Communication)
