#include <cstdlib>
#include <fstream>

extern "C"
{
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
}

int main()
{
	int ret = EXIT_SUCCESS;
	lua_State *L = lua_open();

	// Load the libraries
	luaL_openlibs(L);

	// Execution of a lua string
	luaL_dostring(L, "print \"Goodnight...\"");

	// Load a string and then execute it.
	luaL_loadstring(L, "io.write(\"... moon!\\n\")");
	lua_pcall(L, 0, LUA_MULTRET, 0);

	{
		std::ofstream file("test_package.lua");
		file << "print \"Hello Lua!\"";
	}

	// Load from a file and then execute
	if (luaL_loadfile(L, "test_package.lua") == 0) {
		// File loaded call it
		lua_pcall(L, 0, LUA_MULTRET, 0);
	}
	else
	{
		ret = EXIT_FAILURE;
	}

	// Close lua
	lua_close (L);
	return ret;
}