import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";

const options = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "TSE API Documentation",
            version: "1.0.0",
            description: "API documentation for Email Service, Products, and other routes",
        },
        servers: [
            {
                url: "http://localhost:5000",
                description: "Local Development Server",
            },
        ],
        components: {
            schemas: {}
        },
    },

    apis: [
        "./src/routes/*.js",
        "./src/docs/*.js"
    ],
};

export const swaggerSpec = swaggerJsdoc(options);

export const swaggerDocs = (app) => {
    app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

    console.log("📘 Swagger Docs available at: http://localhost:5000/api-docs");
};
