PREFIX ?= /usr
LIBDIR ?= $(PREFIX)/lib

all:
	@echo Run \'make install\' to install welcome_app.

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	mkdir -p $(DESTDIR)$(LIBDIR)/welcome_app
	cp -p usr/lib/welcome_app/* $(DESTDIR)$(LIBDIR)/welcome_app/
	cp -p usr/bin/welcome_app $(DESTDIR)$(PREFIX)/bin/welcome_app
	chmod 755 $(DESTDIR)$(PREFIX)/bin/welcome_app

uninstall:
	rm -rf $(DESTDIR)$(PREFIX)/bin/welcome_app
	rm -rf $(DESTDIR)$(LIBDIR)/welcome_app*
