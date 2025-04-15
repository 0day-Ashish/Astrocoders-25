import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, Calendar, MapPin, IndianRupee } from "lucide-react";

const events = [
  {
    id: 1,
    title: "Music Fest 2025",
    date: "April 25, 2025",
    location: "Mumbai, India",
    price: "₹4000",
  },
  {
    id: 2,
    title: "Tech Summit 2025",
    date: "May 10, 2025",
    location: "Bangalore, India",
    price: "₹8000",
  },
  {
    id: 3,
    title: "Startup Expo",
    date: "June 15, 2025",
    location: "Delhi, India",
    price: "₹2500",
  },
];

export default function EventResellerApp() {
  return (
    <main className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <motion.h1
            className="text-5xl font-extrabold mb-6 flex items-center justify-center gap-2"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Sparkles className="w-8 h-8 text-yellow-300 animate-pulse" />
            Discover. Resell. Enjoy Events.
          </motion.h1>
          <motion.p
            className="text-lg text-white/80 mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            Find and resell tickets to your favorite concerts, tech summits, and expos.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            <Button className="bg-white text-indigo-600 hover:bg-gray-100 px-6 py-3 text-lg font-medium rounded-xl shadow-md">
              Get Started
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Events Section */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Upcoming Events
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event, idx) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <Card className="hover:shadow-xl transition-shadow duration-300">
                  <CardContent className="p-6 space-y-4">
                    <h3 className="text-xl font-semibold text-gray-700 flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-indigo-500" /> {event.title}
                    </h3>
                    <p className="text-sm text-gray-500 flex items-center gap-1">
                      <Calendar className="w-4 h-4 text-gray-400" /> {event.date}
                    </p>
                    <p className="text-sm text-gray-500 flex items-center gap-1">
                      <MapPin className="w-4 h-4 text-gray-400" /> {event.location}
                    </p>
                    <p className="text-lg font-medium text-green-600 flex items-center gap-1">
                      <IndianRupee className="w-4 h-4" /> {event.price}
                    </p>
                    <Button className="w-full">Buy Ticket</Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t py-6 mt-12 text-center text-gray-500">
        © 2025 Event Reseller. All rights reserved.
      </footer>
    </main>
  );
}
