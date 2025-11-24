'use client';

import { HeroSection } from "@/components/ui/hero";
import { Particles } from "@/components/ui/particles";
import Testimonials from "@/components/ui/Testimonials";
import Footer from "@/components/ui/Footer";

export default function Home() {
  return (
    <div className="scrollbar-hide w-[100%]">
      <Particles className="absolute inset-0 z-10"
        quantity={400}
        ease={10}
        vx={.1}
        vy={.2}
        color="#000000"
        refresh />
      <HeroSection>
      </HeroSection>

      <Testimonials />
      <Footer />
    </div>
  );
}

