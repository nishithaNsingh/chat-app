# Real-time Chat Application with Offline Message Support

A production-ready chat application built with FastAPI, Redis, and PostgreSQL featuring real-time messaging, offline message storage, and typing indicators.

## Features

- **Real-time Messaging**: WebSocket-based real-time communication
- **Offline Message Support**: Messages are stored in Redis when users are offline and delivered when they reconnect
- **Typing Indicators**: Real-time typing status between users
- **Read Receipts**: Track message read status
- **Message History**: Persistent message storage in PostgreSQL
- **User Authentication**: JWT-based authentication
- **Redis Caching**: Performance optimization with Redis caching
- **Active User Tracking**: Track online/offline status in real-time

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (persistent storage)
- **Cache**: Redis (offline messages, sessions, caching)
- **WebSockets**: For real-time communication
- **Authentication**: JWT tokens

## Architecture

### Components

1. **FastAPI Application**: Handles HTTP requests and WebSocket connections
2. **PostgreSQL**: Stores user data and message history
3. **Redis**: 
   - Offline message queue
   - Active user sessions
   - Typing indicators
   - Message caching
4. **WebSocket Manager**: Manages active connections and message routing

### Data Flow

1. **Online Message Flow**:
   - Sender sends message via WebSocket
   - Message stored in PostgreSQL
   - Real-time delivery via WebSocket to receiver

2. **Offline Message Flow**:
   - Sender sends message
   - System checks if receiver is online via Redis
   - If offline, message stored in Redis queue
   - When receiver connects, offline messages are delivered

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- PostgreSQL 14+
- Redis 7+


## 🚀 Deployment

The application is deployed on Render and is publicly accessible.

Base URL: https://chat-app-iwde.onrender.com
