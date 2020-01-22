cmake_minimum_required(VERSION 3.2)
project(lua LANGUAGES C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

option(BUILD_INTERPRETER "Build interpreter" OFF)
option(BUILD_COMPILER "Build compiler" OFF)
option(SHARED "Build a shared library" OFF)

set(LUA_LIB_SOURCES
  src/lapi.c
  src/lcode.c
  src/ldebug.c
  src/ldo.c
  src/ldump.c
  src/lfunc.c
  src/lgc.c
  src/llex.c
  src/lmem.c
  src/lobject.c
  src/lopcodes.c
  src/lparser.c
  src/lstate.c
  src/lstring.c
  src/ltable.c
  src/ltm.c
  src/lundump.c
  src/lvm.c
  src/lzio.c
  src/lauxlib.c
  src/lbaselib.c
  src/ldblib.c
  src/liolib.c
  src/lmathlib.c
  src/loslib.c
  src/ltablib.c
  src/lstrlib.c
  src/loadlib.c
  src/linit.c
)

add_definitions(-DLUA_COMPAT_5_2)

add_library(lua_objects OBJECT ${LUA_LIB_SOURCES})

if(UNIX)
  link_libraries(m)
  target_compile_definitions(lua_objects
    PUBLIC LUA_USE_LINUX
  )
  target_compile_definitions(lua
    PUBLIC LUA_USE_LINUX
  )
endif(UNIX)


if(${SHARED})
  add_library(lua SHARED $<TARGET_OBJECTS:lua_objects>)

  if(MINGW OR WIN32)
    target_compile_definitions(lua_objects
      PUBLIC LUA_BUILD_AS_DLL
    )
    target_compile_definitions(lua
      PUBLIC LUA_BUILD_AS_DLL
    )
  endif(MINGW OR WIN32)
else()
  add_library(lua STATIC $<TARGET_OBJECTS:lua_objects>)
endif()

target_compile_definitions(lua_objects
  PUBLIC LUA_COMPAT_5_2
)
target_compile_definitions(lua
  PUBLIC LUA_COMPAT_5_2
)

if(${BUILD_INTERPRETER})
  add_executable(lua_interpreter src/lua.c src/print.c)
  target_link_libraries(lua_interpreter lua)
  set_target_properties(lua_interpreter PROPERTIES
    OUTPUT_NAME lua
  )
  if(NOT WIN32)
    target_include_directories(lua_interpreter
      PRIVATE ${CONAN_INCLUDE_DIRS_READLINE})
    target_link_libraries(lua_interpreter dl ${CONAN_LIBS_READLINE})
  endif(NOT WIN32)
endif(${BUILD_INTERPRETER})

if(${BUILD_COMPILER})
  add_executable(lua_compiler src/luac.c $<TARGET_OBJECTS:lua_objects>)
  set_target_properties(lua_compiler PROPERTIES
    OUTPUT_NAME luac
  )
endif(${BUILD_INTERPRETER})
