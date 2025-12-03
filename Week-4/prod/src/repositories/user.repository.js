import User from "../models/user.js";
export default class userRepository {
    async create(data) {
        const user = new User(data);
        return await user.save();
    }

    async findById(id) {
        return User.findById(id);
    }

    async findPaginated({ page = 1, limit = 10, filter = {} }) {
        const skip = (page - 1) * limit;
        const data = await User.find(filter)
            .skip(skip)
            .limit(limit)
            .sort({ createdAt: -1 });

        const total = await User.countDocuments(filter);

        return {
            data,
            pagination: {
                page,
                limit,
                total,
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    async update(id, updates) {
        return User.findByIdAndUpdate(id, updates, {
            new: true,
            runValidators: true,
        });
    }

    async delete(id) {
        return User.findByIdAndDelete(id);
    }
}
