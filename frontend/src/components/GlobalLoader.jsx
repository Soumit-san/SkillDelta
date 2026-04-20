import React from 'react';

export default function GlobalLoader() {
    return (
        <div className="w-full h-full flex flex-col items-center justify-start pt-20">
            <div className="relative w-16 h-16">
                {/* Outer glowing ring */}
                <div className="absolute inset-0 rounded-full border-t-2 border-purple-500 border-opacity-50 animate-[spin_1.5s_linear_infinite]"></div>

                {/* Inner solid ring */}
                <div className="absolute inset-2 rounded-full border-r-2 border-b-2 border-red-500 animate-[spin_1s_ease-in-out_infinite_reverse]"></div>

                {/* Core glow */}
                <div className="absolute inset-4 bg-purple-500/20 rounded-full blur-md animate-pulse"></div>
            </div>
        </div>
    );
}
