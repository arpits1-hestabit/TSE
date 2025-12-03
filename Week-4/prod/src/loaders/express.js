import express from "express";

export default function loadExpress(app) {
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
}
