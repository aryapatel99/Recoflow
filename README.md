# 🛍️ RecoFlow

### Event-Driven Personalized Recommendation & Ranking Platform

RecoFlow is a full-stack e-commerce recommendation platform I built to explore how **real-world recommendation systems are designed, built, evaluated, and deployed**.

Instead of building only a recommendation model, RecoFlow connects the entire system together:

**Users → Products → Events → Recommendation Engine → Ranking → Evaluation → Cloud Deployment**

The project is built with **Python, FastAPI, PostgreSQL, Next.js, Docker, and AWS**, with a focus on keeping the architecture practical and production-inspired without adding unnecessary complexity.

---

## 🚀 What is RecoFlow?

Imagine an online store where every action a user takes tells the system something:

- 👀 They view a product
- 🖱️ They click on it
- 🔎 They search for something
- ❤️ They add it to their wishlist
- 🛒 They add it to their cart
- 💳 They purchase it

RecoFlow captures these interactions as events and uses them to generate personalized product recommendations.

The recommendation system combines multiple approaches instead of relying on a single algorithm.

```text
                    👤 User
                       │
                       ▼
              🛍️ E-Commerce UI
                       │
                       ▼
                 ⚡ FastAPI
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Products      Events        Orders
          │            │
          └──────┬─────┘
                 ▼
        🧠 Recommendation Engine
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Popularity  Content   Collaborative
       │         │         │
       └─────────┼─────────┘
                 ▼
          🏆 Hybrid Ranking
                 │
                 ▼
       ⭐ Top-K Recommendations
```

---

# ✨ Key Features

### 🔐 Authentication

RecoFlow includes a proper authentication system instead of treating users as anonymous IDs.

- User registration
- User login
- JWT authentication
- Protected API endpoints
- Password hashing
- Authenticated `/me` endpoint
- Server-side user identity
- Ownership validation

The backend does not blindly trust a `user_id` sent by the frontend for authenticated operations.

---

### 🛍️ Product Catalog

The project uses a real product metadata sample rather than a tiny manually-created demo catalog.

The AWS deployment was seeded with **92 products** containing information such as:

- Product title
- Description
- Price
- Brand
- Category
- Images
- Ratings
- Review counts
- External product IDs

The catalog import process is designed to be **idempotent and non-destructive**, so importing the dataset does not randomly duplicate or remove existing products.

---

# 🧠 Recommendation Engine

The main recommendation logic lives in:

```text
backend/app/ml/recommender.py
```

RecoFlow currently supports four recommendation approaches:

### 🔥 1. Popularity-Based

Recommends products based on overall user interaction activity.

Different events have different weights because a purchase should tell us more than simply viewing a product.

| Event | Weight |
|---|---:|
| `product_view` | 1 |
| `product_click` | 2 |
| `search` | 0.5 |
| `wishlist_add` | 4 |
| `add_to_cart` | 5 |
| `purchase` | 8 |
| `recommendation_impression` | 0.25 |
| `recommendation_click` | 3 |

---

### 🎯 2. Content-Based Recommendation

Looks at the characteristics of products a user has interacted with and finds similar products.

Signals include:

- Product title
- Description
- Brand
- Category
- Product features

This is especially useful when we don't have enough interaction history for a user.

---

### 👥 3. Collaborative Filtering

Uses user-product interaction patterns to find recommendations based on behavior across users.

The idea is simple:

> Users who behave similarly may also be interested in similar products.

---

### 🧩 4. Hybrid Recommendation

RecoFlow combines the different recommendation signals into a single ranking.

Current weights:

```text
Popularity        30%
Content-Based    30%
Collaborative    40%
```

So the current hybrid score is:

```text
Hybrid Score =
    0.30 × Popularity
  + 0.30 × Content Score
  + 0.40 × Collaborative Score
```

Keeping these strategies separate makes it easier to experiment with different ranking approaches later.

---

# ❄️ Cold Start

One of the biggest problems in recommendation systems is the **cold-start problem**.

What should we recommend to someone who just created an account and has no history?

RecoFlow handles this by falling back toward broader signals such as:

- 🔥 Popular products
- 🎯 Content relevance
- 📊 Available interaction data

This means recommendations don't completely break when a user has little or no history.

---

# 📊 Recommendation Evaluation

A recommendation system shouldn't be judged only by looking at a few recommendations and saying:

> "Looks good."

RecoFlow includes an offline evaluation workflow to measure recommendation quality.

Current metrics include:

- **Precision@K**
- **Recall@K**
- **NDCG@K**
- **MAP@K**
- **Coverage**
- **Diversity**

The evaluation follows a temporal / leave-last-event-out style approach so that the system can be evaluated using historical behavior rather than simply training and testing on the same interactions.

---

# ⚡ Event-Driven Design

User behavior is represented through events.

Supported events include:

```text
product_view
product_click
search
add_to_cart
purchase
wishlist_add
recommendation_impression
recommendation_click
```

Each event can contain:

- Event ID
- User ID
- Session ID
- Event type
- Product ID
- Event timestamp
- Received timestamp
- Metadata

This event layer becomes the foundation for personalization and future feature engineering.

---

# 🛒 Cart & Checkout

RecoFlow isn't just a recommendation demo.

It also includes a real shopping workflow:

```text
Browse Products
      ↓
Add to Cart
      ↓
Review Cart
      ↓
Checkout
      ↓
Create Order
      ↓
Record Purchase Event
      ↓
Clear Cart
```

Important business logic is handled by the backend.

For example:

- Product prices are validated server-side
- Order totals are calculated server-side
- Users can only access their own orders
- Checkout supports idempotency
- Successful purchases generate behavioral events

The frontend isn't trusted to decide what an order should cost.

---

# 🎨 Frontend

The frontend is built to feel like an actual shopping platform rather than a basic ML dashboard.

### Tech

- ⚛️ React
- ▲ Next.js
- 🔷 TypeScript
- 🎨 Tailwind CSS
- ✨ Framer Motion
- 🎯 Lucide
- 🌐 Three.js / React Three Fiber

The UI includes:

- 🏠 Product discovery
- 🔎 Search
- 🛍️ Product cards
- 📦 Product details
- ❤️ Wishlist
- 🛒 Cart
- 💳 Checkout
- 👤 Authentication
- ⭐ Recommendations
- 📱 Responsive layouts
- ⏳ Loading states
- ⚠️ Error states

The goal was to make the project feel like a **real product**, not just a project dashboard.

---

# 🏗️ Backend Architecture

The backend is built using:

- 🐍 Python
- ⚡ FastAPI
- 🗄️ PostgreSQL
- 🔧 SQLAlchemy
- 🔄 Alembic
- 🔐 JWT
- 📦 Pydantic

The project follows a **modular monolith** architecture.

```text
backend/
└── app/
    ├── api/
    ├── core/
    ├── db/
    ├── ml/
    ├── models/
    ├── schemas/
    └── services/
```

I intentionally chose a modular monolith instead of immediately introducing microservices.

Why?

Because the goal is to first build a system that is:

- Easy to understand
- Easy to test
- Easy to deploy
- Easy to debug
- Easy to explain

If the system eventually needs service decomposition, the modules provide a reasonable starting point.

---

# 🚫 Why Not Kafka / Kubernetes / Microservices?

RecoFlow deliberately avoids adding infrastructure just to make the architecture look complicated.

There is currently no need to introduce:

- Kafka
- Kubernetes
- Service mesh
- Multiple microservices

The project focuses first on getting the fundamentals right:

```text
Good API Design
      +
Good Database Design
      +
Authentication
      +
Event Processing
      +
Recommendation Logic
      +
ML Evaluation
      +
Cloud Deployment
```

Complexity should be introduced when the system actually needs it.

---

# 🗄️ Database

RecoFlow uses **PostgreSQL** as its primary database.

The database stores information for:

- Users
- Products
- Categories
- User events
- Recommendations
- Carts
- Cart items
- Orders
- Order items
- Model metadata
- Supporting application data

Database schema changes are managed using **Alembic**.

Current migrations:

```text
0001_initial_schema
0002_authentication
0003_checkout_order_details
0004_remove_email_verification
```

Current migration head:

```text
0004_remove_email_verification
```

---

# 🧪 Testing & Validation

I didn't want the project to work only on my machine.

The project has been tested across the backend, database, frontend, Docker, and AWS deployment.

### Backend

```text
26 tests
0 failures
0 skipped
```

### Database validation

Checks included:

- Product integrity
- Duplicate external IDs
- Invalid prices
- Orphan order items
- Orphan events
- Empty product titles

### Frontend

Validated:

- TypeScript
- Production build
- Routes
- API integration

### Docker

Validated:

- Backend image
- Frontend image
- Non-root containers
- Container health checks

---

# ☁️ AWS Deployment

RecoFlow was also deployed to AWS to move beyond a purely local project.

The AWS architecture uses:

```text
                    🌍 Internet
                        │
                        ▼
               Application Load Balancer
                        │
                        ▼
                  ECS Fargate
                 ┌───────────┐
                 │ Frontend  │
                 │ Next.js   │
                 ├───────────┤
                 │ Backend   │
                 │ FastAPI   │
                 └─────┬─────┘
                       │
                       ▼
                Amazon RDS
                 PostgreSQL
```

---

# ☁️ AWS Services Used

### 🐳 Amazon ECS Fargate

Runs the RecoFlow application containers without managing servers.

---

### 📦 Amazon ECR

Stores the Docker images:

```text
recoflow-backend
recoflow-frontend
```

---

### 🗄️ Amazon RDS

Hosts the PostgreSQL database.

Deployment configuration included:

```text
PostgreSQL
db.t4g.micro
20 GB storage
Encryption enabled
Public access disabled
Backups enabled
```

---

### 🌐 Application Load Balancer

Routes internet traffic to the frontend container.

```text
Internet
   ↓
ALB :80
   ↓
Next.js :3001
```

---

### 🔐 AWS Secrets Manager

Sensitive configuration such as:

- Database credentials
- Database connection information
- JWT secret

is stored outside the source code.

---

### 🔑 IAM

IAM roles are used to give AWS services the permissions they actually need.

---

# 🤖 AWS ML Roadmap

The recommendation engine currently runs as part of the application.

The next stage is to move more of the ML lifecycle into AWS using **Amazon SageMaker**.

Planned architecture:

```text
User Events
     ↓
Feature / Dataset Preparation
     ↓
Amazon S3
     ↓
SageMaker Training
     ↓
Model Artifact
     ↓
Evaluation
     ↓
Model Versioning
     ↓
Deployment
     ↓
Recommendation System
```

The important idea is that the project isn't just about training a model.

It is about building the surrounding ML engineering workflow as well.

---

# 🧠 ML Engineering Focus

RecoFlow is designed around practical ML engineering concepts:

- Feature generation
- Behavioral data
- Candidate generation
- Ranking
- Cold-start handling
- Offline evaluation
- Model metadata
- Model versioning
- Dataset versioning
- Model artifacts
- Cloud-based ML workflows
- Future MLOps integration

---

# 📦 Model Metadata

RecoFlow stores metadata about recommendation models, including:

```text
model_name
model_version
strategy
dataset_version
artifact_location
training_timestamp
status
created_at
```

This provides a foundation for tracking which model/version produced a recommendation.

---

# 🐳 Docker

Both backend and frontend have their own Dockerfiles.

### Backend

```text
Python 3.12
FastAPI
Uvicorn
```

### Frontend

```text
Node.js 22
Next.js
```

Both containers are configured to run as non-root users.

---

# 🔄 Local Development

## 1️⃣ Clone the repository

```bash
git clone https://github.com/aryapatel99/Recoflow.git
cd Recoflow
```

---

## 2️⃣ Backend

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your local environment variables.

---

## 3️⃣ Database

Create the PostgreSQL database:

```text
recoflow
```

Configure:

```text
DATABASE_URL
```

Run migrations:

```bash
alembic upgrade head
```

---

## 4️⃣ Start the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 5️⃣ Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3001
```

---

# 📡 Behavior Simulation

RecoFlow includes tooling for generating realistic user behavior.

The simulator interacts with the **actual application API** instead of directly inserting fake rows into PostgreSQL.

That means the flow remains:

```text
Simulator
    ↓
API
    ↓
Authentication
    ↓
Event Processing
    ↓
Database
    ↓
Recommendation System
```

This makes the generated data much closer to how a real application would produce it.

---

# 📈 Recommendation Flow

A typical recommendation request looks like this:

```text
👤 Authenticated User
          ↓
📚 User History
          ↓
🎯 Candidate Generation
          ↓
🚫 Filtering
          ↓
🧮 Score Calculation
          ↓
🏆 Ranking
          ↓
⭐ Top-K Recommendations
```

---

# 📁 Project Structure

```text
Recoflow/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── ml/
│       ├── models/
│       ├── schemas/
│       └── services/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── alembic/
│   └── versions/
│
├── data/
│   └── raw/
│
├── deployment/
│   ├── aws/
│   ├── backend/
│   ├── database/
│   ├── docs/
│   ├── frontend/
│   └── scripts/
│
├── scripts/
│
├── requirements.txt
├── alembic.ini
├── README.md
└── .gitignore
```

---

# 🚀 Deployment Documentation

AWS deployment-related documentation is located inside:

```text
deployment/
```

It includes:

```text
deployment/
├── README.md
├── .env.example
├── .gitignore
│
├── aws/
│   ├── README.md
│   ├── credentials.example
│   ├── config.example
│   └── iam/
│
├── backend/
│   ├── README.md
│   └── Dockerfile
│
├── frontend/
│   ├── README.md
│   └── Dockerfile
│
├── database/
│   ├── README.md
│   └── migrations.md
│
├── scripts/
│   ├── deploy-backend.ps1
│   ├── deploy-frontend.ps1
│   ├── deploy.ps1
│   ├── verify-aws.ps1
│   └── health-check.ps1
│
└── docs/
    ├── architecture.md
    ├── aws-services.md
    ├── environment-variables.md
    ├── secrets.md
    ├── rollback.md
    └── deployment-checklist.md
```

---

# 💰 Cost-Aware AWS Development

Cloud resources cost money even when you're not actively using the application.

So the project follows a simple workflow:

```text
💻 Build Locally
      ↓
🧪 Test Locally
      ↓
🐳 Validate Docker
      ↓
☁️ Deploy to AWS
      ↓
🔍 Validate
      ↓
🛑 Stop / Clean Up Resources
```

AWS is used where it adds engineering value rather than simply adding cloud services for the sake of having them.

---

# 📌 Current Status

### ✅ Completed

- [x] Project architecture
- [x] Dataset selection
- [x] PostgreSQL schema
- [x] Alembic migrations
- [x] JWT authentication
- [x] Product catalog
- [x] Event system
- [x] Cart
- [x] Checkout
- [x] Order validation
- [x] Popularity recommendations
- [x] Content-based recommendations
- [x] Collaborative filtering
- [x] Hybrid recommendations
- [x] Cold-start handling
- [x] Recommendation evaluation
- [x] E-commerce frontend
- [x] Dockerization
- [x] Amazon ECR
- [x] Amazon ECS Fargate
- [x] Amazon RDS PostgreSQL
- [x] AWS Secrets Manager
- [x] IAM configuration
- [x] Application Load Balancer
- [x] AWS deployment validation
- [x] Deployment documentation

### 🔜 Next

- [ ] Amazon S3 dataset pipeline
- [ ] SageMaker training jobs
- [ ] SageMaker processing
- [ ] Model artifact management
- [ ] Model versioning
- [ ] Automated ML pipeline
- [ ] Model monitoring
- [ ] Data drift monitoring
- [ ] Recommendation A/B testing
- [ ] Improved ranking models

---

# 🧭 Design Decisions

A few decisions were made intentionally throughout the project.

### 🧱 Modular Monolith First

I wanted to understand the system before introducing distributed infrastructure.

### 🐍 Python-First Backend

Python works well across the API, recommendation, data processing, and ML parts of the project.

### 🗄️ PostgreSQL

A relational database provides a strong foundation for users, products, orders, and behavioral events.

### ⚡ Event-Driven Core

User behavior is represented as events so recommendation logic can evolve as more data becomes available.

### 📊 Measure Instead of Guess

Recommendation quality is evaluated with actual metrics rather than only looking at sample outputs.

### ☁️ Local First → AWS

The application is developed and tested locally before moving components to AWS.

### 🚫 Avoid Premature Complexity

Technologies such as Kafka, Kubernetes, microservices, and deep learning are not added unless they solve an actual problem in the system.

---

# 🛠️ Tech Stack

### Backend

🐍 Python  
⚡ FastAPI  
🗄️ PostgreSQL  
🔧 SQLAlchemy  
🔄 Alembic  
🔐 JWT  
📦 Pydantic  

### Frontend

▲ Next.js  
⚛️ React  
🔷 TypeScript  
🎨 Tailwind CSS  
✨ Framer Motion  
🎯 Lucide  
🌐 Three.js / React Three Fiber  

### ML

🐍 Python  
🎯 Content-Based Filtering  
👥 Collaborative Filtering  
🔥 Popularity Ranking  
🧩 Hybrid Recommendation  
📊 Offline Evaluation  

### AWS

☁️ Amazon ECS Fargate  
📦 Amazon ECR  
🗄️ Amazon RDS  
🔐 AWS Secrets Manager  
🔑 AWS IAM  
🌐 Application Load Balancer  
🪣 Amazon S3  
🤖 Amazon SageMaker roadmap  

### Development

🐳 Docker  
🔧 Git  
🐙 GitHub  
💻 PowerShell  
☁️ AWS CLI  

---

# 🎯 What I Wanted to Learn From This Project

RecoFlow was built to go beyond simply saying:

> "I built a recommendation model."

The goal was to understand how the pieces fit together:

```text
Software Engineering
        ↓
Backend Development
        ↓
Database Design
        ↓
Event Processing
        ↓
Recommendation Systems
        ↓
ML Evaluation
        ↓
Docker
        ↓
AWS
        ↓
ML Engineering / MLOps
```

The recommendation algorithm is only one part of the system.

The real challenge is building everything around it.

---

# 👨‍💻 Author

## Arya Patel


Integrated Master of Computer Applications (IMCA)

Interested in:

- 💻 Software Engineering
- ⚙️ Backend Engineering
- ☁️ Cloud Engineering
- 🤖 AI / ML Engineering
- 📊 ML Systems
- 🚀 MLOps

---

# ⭐ Final Note

RecoFlow is a project built around a simple idea:

> **Don't just build the model. Build the system around the model.**

A recommendation system needs more than an algorithm.

It needs:

```text
👤 Users
+
🛍️ Products
+
⚡ Events
+
🗄️ Data
+
🔌 APIs
+
🧠 Recommendation Logic
+
📊 Evaluation
+
🔐 Security
+
🐳 Deployment
+
☁️ Infrastructure
+
🤖 ML Engineering
```

And that's what RecoFlow is trying to bring together.
```

