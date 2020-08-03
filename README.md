# Introduction 
Third party libraries: openscenegraph

This package has been adapted from the public recipe at bincrafters
https://github.com/bincrafters/conan-openscenegraph

A substantial change is that the package exports the contents of the src/osgPlugins/freetype folder.
This is not OpenSceneGraph public API but is used by vislib_kernel to accurately map Freetype font references to QFont references without breaking because both QFont and OpenSceneGraph think they are the only users of the Freetype font resource.
We use the resulting source code to access this private implementation detail. We shouldn't really but undoing this requires a project in it's own right.
