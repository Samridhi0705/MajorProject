# System Architecture Diagram Specification

## Overview
This document provides the specifications for the system architecture diagram of the MajorProject. It outlines the components, their interactions, and the overall structure of the system.

## Components
1. **Front-end**
   - Description: The user interface of the application.
   - Technologies: React.js, HTML, CSS.

2. **Back-end**
   - Description: The server-side logic that processes user requests.
   - Technologies: Node.js, Express.

3. **Database**
   - Description: The storage for user data and application information.
   - Technologies: MongoDB.

4. **API Gateway**
   - Description: Manages requests from clients to the appropriate services.
   - Technologies: Nginx.

## Interactions
- Front-end communicates with the back-end using RESTful APIs.
- Back-end interacts with the database to save and retrieve data.
- API Gateway routes requests between clients and the back-end.

## Deployment
- The application will be deployed on AWS, utilizing services such as EC2 for hosting and S3 for static file storage.

## Diagram
- A visual representation of the system will be created using tools like Lucidchart or Draw.io and appended to this document once completed.

## Conclusion
This specification serves as the foundation for developing the system architecture diagram, ensuring all stakeholders have a clear understanding of the system's structure.