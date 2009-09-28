28-09-2009: Domen Kozar v0.3.5
------------------------------

	* added `timestamp` parameter [thanks to bobf]

10-06-2009: Domen Kozar v0.3.4
------------------------------

	* finally refactored custom cssutils serializer, threw out some stuff and fixed bugs.

10-06-2009: Domen Kozar v0.3.3
------------------------------

	* fix compatibility with Windows platform (os.path)

09-06-2009: Domen Kozar v0.3.2
------------------------------

	* added `combined_filename` parameter
	* fixed a bug when two paths were similar and resulted in IOError

22-05-2009: Domen Kozar v0.3.1
------------------------------

  * updated documentation
  * added `beaker_kwargs` option to both function that overrides default caching behaviour
  * fixed a bug when paths were not joined correctly
  * written unittests

04-05-2009: Domen Kozar v0.3.0
------------------------------

  * fixed a bug when sources were not invalidated (in cache) on startup
  * complete refactoring

16-04-2009: Domen Kozar v0.2.1
------------------------------

	* replaced deprecated rails functions with new webhelpers.html package
	* added invalidate_on_startup=True argument to beaker.cache

02-02-2007: Pedro Algarvio v0.2.0
---------------------------------

	* Included the fix implemented on [110], wasn't included on trunk.
	* Skip minification/combination when requesting builtin javascripts.
