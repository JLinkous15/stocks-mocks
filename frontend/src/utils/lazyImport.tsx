import { lazy } from 'react'

export const lazyImport = (path: string, namedExport: string) => {
  return lazy(() => {
    const promise = import(/* @vite-ignore */ path)
    if (namedExport) {
      return promise.then((module) => ({ default: module[namedExport] }))
    } else {
      return promise
    }
  })
}

//alt ?

// export const viteLazyImport = () => {
//   return lazy(() => {
//     let modules = import.meta.glob("../panels/Todos/Todos.tsx", {import: "Todos"})
//      return modules["Todos"]().default
//   })
// }

// console.log(viteLazyImport())
