import Image from "next/image";
export default function ProfileDetail({
    image,
    name,
    jobTitle,
    email,
    linkedin,
    twitter,
    facebook,
    bio,
}) {
    return (
        <div className="max-w-5xl mx-auto p-6 bg-white rounded-lg mt-20 shadow">
            {/* Back button */}
            <button
                onClick={() => window.history.back()}
                className="text-blue-600 text-sm mb-4 flex items-center gap-1 hover:underline"
            >
                ← Go back
            </button>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {/* Left: Profile Image */}
                <div className="md:col-span-1 flex justify-center md:block">
                    <Image
                        src={image}
                        alt="Arpit Saxena"
                        width={200}
                        height={200}
                        className="rounded-full"
                    />
                </div>

                <div className="md:col-span-2 space-y-4">
                    <div>
                        <p className="text-sm text-gray-500">Name</p>
                        <p className="text-lg font-semibold">{name}</p>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Job Title</p>
                        <p className="text-md">{jobTitle}</p>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Email</p>
                        <p className="text-blue-600 hover:underline cursor-pointer">
                            {email}
                        </p>
                    </div>
                </div>

                <div className="md:col-span-1 space-y-4">
                    <div>
                        <p className="text-sm text-gray-500">LinkedIn</p>
                        <a href={linkedin} className="text-blue-600 hover:underline">
                            {linkedin.replace("https://", "")}
                        </a>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Twitter</p>
                        <a href={twitter} className="text-blue-600 hover:underline">
                            {twitter.replace("https://", "")}
                        </a>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Facebook</p>
                        <a href={facebook} className="text-blue-600 hover:underline">
                            {facebook.replace("https://", "")}
                        </a>
                    </div>
                </div>
            </div>

            <div className="mt-6">
                <p className="text-sm text-gray-500 mb-1">Bio</p>
                <p className="text-gray-700 leading-relaxed">{bio}</p>
            </div>

            <button className="mt-4 text-blue-600 hover:underline">
                Edit Profile
            </button>
        </div>
    );
}
