'use client';

import { TextAnimate } from "@/components/ui/text-animate";
import { TypingAnimation } from "@/components/ui/typing-animation";
import { AuroraText } from "@/components/ui/aurora-text";
import { BorderBeam } from "@/components/ui/border-beam";
import { Particles } from "@/components/ui/particles";
import Ratings from "./Ratings";
import Testimonials from "./Testimonials";
import Footer from "./Footer";

export function HeroSection() {
    return (
        <section className="relative w-screen h-screen overflow-hidden bg-gradient-to-br from-gray-50 via-purple-50 to-purple-100 text-gray-900">

            <Particles className="absolute inset-0 -z-10" width="100%" height="100%" />

            <div className="absolute inset-0 flex flex-col items-center justify-center px-4 md:px-0 text-center max-w-2xl mx-auto gap-6 z-20">

                <TextAnimate
                    animation="blurInUp"
                    by="word"
                    duration={0.7}
                    className="text-4xl md:text-6xl font-extrabold"
                >
                    Welcome to Your
                </TextAnimate>

                <AuroraText className="text-4xl md:text-6xl font-extrabold">
                    Dashboard
                </AuroraText>


                <TypingAnimation
                    typeSpeed={100}
                    className="text-lg md:text-xl font-semibold mt-4"
                >
                    Track your metrics, manage your data, and stay on top of everything.
                </TypingAnimation>

                <div className="relative inline-block mt-6">
                    <div className="absolute -inset-1 rounded-lg overflow-hidden">
                        <BorderBeam />
                    </div>

                    <a
                        href="/dashboard"
                        className="relative z-10 inline-block px-6 py-3 rounded-lg bg-purple-600 text-white font-bold text-lg hover:bg-purple-700 transition-colors"
                    >
                        Go to Dashboard
                    </a>
                </div>
                <Ratings />
                {/* <Testimonials /> */}
                {/* <Footer /> */}
            </div>

        </section>

    );
}
