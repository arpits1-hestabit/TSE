import mongoose from "mongoose";
const ProductSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      minlength: 2,
    },
    description: {
      type: String,
      trim: true,
    },
    price: {
      type: Number,
      required: true,
      min: [0, "Price must be positive"],
      get: (value) => Number(value.toFixed(2)),
      set: (value) => Number(value.toFixed(2)),
    },
    rating: {
      type: Number,
      default: 0,
      min: 0,
      max: 5,
    },

  },
  {
    strict: false
  }
);

ProductSchema.index({ status: 1, createdAt: -1 });

const Product = mongoose.model("Product", ProductSchema);

export default Product;
