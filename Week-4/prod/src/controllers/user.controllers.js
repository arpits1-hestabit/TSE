const UserRepository = require("../repositories/user.repository");
const UserService = require("../services/user.service");
const { logger } = require("../utils/logger");

class UserController {

    // get all users
  static async getAllUsers(req, res, next) {
    try {
      const users = await UserRepository.findAll();
      res.status(200).json({
        success: true,
        data: users,
        message: "Users retrieved successfully",
      });
    } catch (error) {
      logger.error("Error fetching users", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }

 // get user by id
  static async getUserById(req, res, next) {
    try {
      const { id } = req.params;
      const user = await UserRepository.findById(id);

      if (!user) {
        return res.status(404).json({
          success: false,
          message: "User not found",
        });
      }

      res.status(200).json({
        success: true,
        data: user,
        message: "User retrieved successfully",
      });
    } catch (error) {
      logger.error("Error fetching user by ID", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }

  // create new user
  static async createUser(req, res, next) {
    try {
      const userData = req.body;
      const newUser = await UserService.createUser(userData);

      res.status(201).json({
        success: true,
        data: newUser,
        message: "User created successfully",
      });
    } catch (error) {
      logger.error("Error creating user", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }

  // update user
  static async updateUser(req, res, next) {
    try {
      const { id } = req.params;
      const updateData = req.body;
      const updatedUser = await UserService.updateUser(id, updateData);

      if (!updatedUser) {
        return res.status(404).json({
          success: false,
          message: "User not found",
        });
      }

      res.status(200).json({
        success: true,
        data: updatedUser,
        message: "User updated successfully",
      });
    } catch (error) {
      logger.error("Error updating user", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }

  // delete user
  static async deleteUser(req, res, next) {
    try {
      const { id } = req.params;
      const result = await UserService.deleteUser(id);

      if (!result) {
        return res.status(404).json({
          success: false,
          message: "User not found",
        });
      }

      res.status(200).json({
        success: true,
        message: "User deleted successfully",
      });
    } catch (error) {
      logger.error("Error deleting user", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }

  // get user profile
  static async getUserProfile(req, res, next) {
    try {
      const userId = req.user?.id;
      const profile = await UserRepository.findById(userId);

      if (!profile) {
        return res.status(404).json({
          success: false,
          message: "User profile not found",
        });
      }

      res.status(200).json({
        success: true,
        data: profile,
        message: "User profile retrieved successfully",
      });
    } catch (error) {
      logger.error("Error fetching user profile", {
        error: error.message,
        requestId: req.id,
      });
      next(error);
    }
  }
}

module.exports = UserController;
