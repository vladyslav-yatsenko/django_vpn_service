# Django VPN Service

This project implements a simple VPN service as a web application. Clients can register, access their personal dashboard, edit personal information, and create websites. The service acts as a proxy for websites, allowing users to navigate them securely through an internal routing mechanism.

## Features

1. User Registration: Clients can register on the website to gain access to their personal dashboard.

2. Personal Dashboard:
   - Edit Personal Information: Users can edit their personal details.
   - Website Statistics: Display statistics, including the number of page transitions divided by websites and the volume of data sent and received per website.

3. Website Management:
   - Create websites.
   - Clicking "Go to Website" redirects the user to an internal route acting as a proxy to the original site.

    
## Installation

### 1. Clone this repository to your local machine.

### 2. Build docker

```bash
$ docker compose build
```

### 3. Run migrations

```bash
$ docker compose run server python manage.py migrate
```

### 4. Create superuser

```bash
$ docker compose run server python manage.py createsuperuser
```

### 5. Run container

```bash
$ docker compose up
```

## Usage

### Registration

```bash
http://127.0.0.1:8000/register/
```

### Login

```bash
http://127.0.0.1:8000/login/
```

### Main page

```bash
http://127.0.0.1:8000/home/
```

### Edit Profile

```bash
http://127.0.0.1:8000/profile/
```

### Site statistics

```bash
http://127.0.0.1:8000/user_site_statistics/
```

### Create new site

```bash
http://127.0.0.1:8000/create_site/
```
