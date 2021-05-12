<h1>Blog application</h1>

[![test](https://github.com/DramatikMan/blog-application/actions/workflows/test.yml/badge.svg)](https://github.com/DramatikMan/blog-application/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/DramatikMan/blog-application/branch/main/graph/badge.svg?token=FZKPN2B08Y)](https://codecov.io/gh/DramatikMan/blog-application)
[![build](https://github.com/DramatikMan/blog-application/actions/workflows/build.yml/badge.svg)](https://github.com/users/DramatikMan/packages/container/package/blog-application)

⚱ Flask application showcase.<br>

Current deployment setup:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog-application
  labels:
    app: blog-application
spec:
  replicas: 2
  selector:
    matchLabels:
      app: blog-application
  template:
    metadata:
      labels:
        app: blog-application
    spec:
      containers:
      - name: blog-application
        image: ghcr.io/dramatikman/blog-application
        ports:
        - containerPort: 8000
        env:
          - name: SCRIPT_NAME
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: SCRIPT_NAME
          - name: FLASK_APP
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: FLASK_APP
          - name: FLASK_ENV
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: FLASK_ENV
          - name: POSTGRES_USER
            valueFrom:
              secretKeyRef:
                name: postgres
                key: POSTGRES_USER
          - name: POSTGRES_PASSWORD
            valueFrom:
              secretKeyRef:
                name: postgres
                key: POSTGRES_PASSWORD
          - name: POSTGRES_HOST
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: POSTGRES_HOST
          - name: POSTGRES_PORT
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: POSTGRES_PORT
          - name: POSTGRES_DB
            valueFrom:
              configMapKeyRef:
                name: blog-application
                key: POSTGRES_DB
          - name: SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: SECRET_KEY
          - name: RECAPTCHA_PUBLIC_KEY
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: RECAPTCHA_PUBLIC_KEY
          - name: RECAPTCHA_PRIVATE_KEY
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: RECAPTCHA_PRIVATE_KEY
          - name: GOOGLE_OAUTH_CLIENT_ID
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: GOOGLE_OAUTH_CLIENT_ID
          - name: GOOGLE_OAUTH_CLIENT_SECRET
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: GOOGLE_OAUTH_CLIENT_SECRET
          - name: ADMIN_NAME
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: ADMIN_NAME
          - name: ADMIN_PASSWORD
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: ADMIN_PASSWORD
          - name: ADMIN_EMAIL
            valueFrom:
              secretKeyRef:
                name: blog-application
                key: ADMIN_EMAIL
---
apiVersion: v1
kind: Service
metadata:
  name: blog-application
spec:
  selector:
    app: blog-application
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```