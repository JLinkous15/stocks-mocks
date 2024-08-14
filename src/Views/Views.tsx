import React from "react"

interface ViewWrapperProps {
  children: React.ReactNode
}

export function Views({children}: ViewWrapperProps) {
  return <>{children}</>
}