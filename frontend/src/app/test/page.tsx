'use client'

export default function TestPage() {
  return (
    <div className="min-h-screen p-8 bg-white dark:bg-gray-900">
      <h1 className="text-2xl font-bold text-black dark:text-white">Test Page</h1>
      <p className="mt-4 text-gray-600 dark:text-gray-400">If you can see this, the basic Next.js setup is working.</p>
      <div className="mt-8 p-4 bg-green-100 dark:bg-green-900 rounded">
        <p className="text-green-800 dark:text-green-200">✅ React components are rendering</p>
        <p className="text-green-800 dark:text-green-200">✅ Tailwind CSS is working</p>
        <p className="text-green-800 dark:text-green-200">✅ Client-side rendering is active</p>
      </div>
    </div>
  )
}