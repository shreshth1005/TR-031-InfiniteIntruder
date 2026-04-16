"use client";

import { Canvas } from "@react-three/fiber";
import { Float, Sphere, MeshDistortMaterial, Stars } from "@react-three/drei";

function Orb({ position, scale, color }) {
  return (
    <Float speed={1.5} rotationIntensity={0.5} floatIntensity={1}>
      <Sphere args={[1, 64, 64]} position={position} scale={scale}>
        <MeshDistortMaterial color={color} distort={0.18} speed={1.2} roughness={0.2} />
      </Sphere>
    </Float>
  );
}

export default function Hero3D() {
  return (
    <div className="absolute inset-0 opacity-40">
      <Canvas camera={{ position: [0, 0, 9], fov: 55 }}>
        <ambientLight intensity={1.1} />
        <directionalLight position={[3, 3, 3]} intensity={1.5} />
        <Stars radius={70} depth={25} count={2500} factor={3} fade />

        <Orb position={[-3.2, 0.8, -1]} scale={1.1} color="#1e3a8a" />
        <Orb position={[3.2, -0.5, -2]} scale={0.9} color="#334155" />
        <Orb position={[0.6, 2, -3]} scale={0.6} color="#d4af37" />
      </Canvas>

      <div className="absolute inset-0 bg-gradient-to-b from-[#0b1120]/20 via-[#0b1120]/40 to-[#0b1120]" />
    </div>
  );
}