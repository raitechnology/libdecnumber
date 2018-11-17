lsb_dist     := $(shell if [ -x /usr/bin/lsb_release ] ; then lsb_release -is ; else echo Linux ; fi)
lsb_dist_ver := $(shell if [ -x /usr/bin/lsb_release ] ; then lsb_release -rs | sed 's/[.].*//' ; fi)
uname_m      := $(shell uname -m)

short_dist_lc := $(patsubst CentOS,rh,$(patsubst RedHat,rh,\
                   $(patsubst Fedora,fc,$(patsubst Ubuntu,ub,\
                     $(patsubst Debian,deb,$(patsubst SUSE,ss,$(lsb_dist)))))))
short_dist    := $(shell echo $(short_dist_lc) | tr a-z A-Z)
rpm_os        := $(short_dist_lc)$(lsb_dist_ver).$(uname_m)

# this is where the targets are compiled
build_dir ?= $(short_dist)$(lsb_dist_ver)_$(uname_m)$(port_extra)
bind      := $(build_dir)/bin
libd      := $(build_dir)/lib64
objd      := $(build_dir)/obj
dependd   := $(build_dir)/dep

major_num   := 3
minor_num   := 61
patch_num   := 0
build_num   := 1
version     := $(major_num).$(minor_num).$(patch_num)
ver_build   := $(version)-$(build_num)

CC       ?= gcc
AR       ?= ar
CFLAGS   ?= -ggdb -O2 -Wall -fPIC
INCLUDES ?= -Isrc -Iinclude/libdecnumber -Iinclude/libdecnumber/bid \
            -Iinclude/libdecnumber/dpd
cc       := $(CC)
cflags   := $(CFLAGS)
includes := $(INCLUDES)
defines  :=
soflag   := -shared

everything: all

libdecnumber_files := decNumber decContext decimal32 decimal64 decimal128 \
                      bid2dpd_dpd2bid host-ieee32 host-ieee64 host-ieee128
libdecnumber_objs  := $(addprefix $(objd)/, $(addsuffix .o, $(libdecnumber_files)))
libdecnumber_dbjs  := $(addprefix $(objd)/, $(addsuffix .fpic.o, $(libdecnumber_files)))
libdecnumber_deps  := $(addprefix $(dependd)/, $(addsuffix .d, $(libdecnumber_files))) \
                     $(addprefix $(dependd)/, $(addsuffix .fpic.d, $(libdecnumber_files)))
libdecnumber_spec  := $(version)-$(build_num)
libdecnumber_ver   := $(major_num).$(minor_num)

$(libd)/libdecnumber.a: $(libdecnumber_objs)

$(libd)/libdecnumber.so: $(libdecnumber_dbjs)

all_depends += $(libdecnumber_deps)
all_dirs    += $(bind) $(libd) $(objd) $(dependd)
all_libs    += $(libd)/libdecnumber.a $(libd)/libdecnumber.so

all: $(all_libs)

# create directories
$(dependd):
	@mkdir -p $(all_dirs)

# remove target bins, objs, depends
.PHONY: clean
clean:
	rm -r -f $(bind) $(libd) $(objd) $(dependd)
	if [ "$(build_dir)" != "." ] ; then rmdir $(build_dir) ; fi

$(dependd)/depend.make: $(dependd) $(all_depends)
	@echo "# depend file" > $(dependd)/depend.make
	@cat $(all_depends) >> $(dependd)/depend.make

.PHONY: dist_bins
dist_bins: $(all_libs)

.PHONY: dist_rpm
dist_rpm:
	mkdir -p rpmbuild/{RPMS,SRPMS,BUILD,SOURCES,SPECS}
	sed -e "s/99999/${build_num}/" \
	    -e "s/999.999/${version}/" < rpm/libdecnumber.spec > rpmbuild/SPECS/libdecnumber.spec
	mkdir -p rpmbuild/SOURCES/libdecnumber-${version}
	ln -sf ../../../src ../../../include ../../../GNUmakefile rpmbuild/SOURCES/libdecnumber-${version}/
	( cd rpmbuild/SOURCES && tar chzf libdecnumber-${ver_build}.tar.gz --exclude=".*.sw*" libdecnumber-${version} && rm -r -f libdecnumber-${version} )
	( cd rpmbuild && rpmbuild --define "-topdir `pwd`" -ba SPECS/libdecnumber.spec )

# force a remake of depend using 'make -B depend'
.PHONY: depend
depend: $(dependd)/depend.make

# dependencies made by 'make depend'
-include $(dependd)/depend.make

$(objd)/%.o: src/%.c
	$(cc) $(cflags) $(includes) $(defines) $($(notdir $*)_includes) $($(notdir $*)_defines) -c $< -o $@

$(objd)/%.o: src/bid/%.c
	$(cc) $(cflags) $(includes) $(defines) $($(notdir $*)_includes) $($(notdir $*)_defines) -c $< -o $@

$(objd)/%.fpic.o: src/%.c
	$(cc) $(cflags) $(fpicflags) $(includes) $(defines) $($(notdir $*)_includes) $($(notdir $*)_defines) -c $< -o $@

$(objd)/%.fpic.o: src/bid/%.c
	$(cc) $(cflags) $(fpicflags) $(includes) $(defines) $($(notdir $*)_includes) $($(notdir $*)_defines) -c $< -o $@

$(libd)/%.a:
	ar rc $@ $($(*)_objs)

$(libd)/%.so:
	$(cc) $(soflag) $(cflags) -o $@.$($(*)_spec) -Wl,-soname=$(@F).$($(*)_ver) $($(*)_dbjs) $($(*)_dlnk) $(cpp_dll_lnk) $(sock_lib) $(math_lib) $(thread_lib) $(malloc_lib) $(dynlink_lib) && \
	cd $(libd) && ln -f -s $(@F).$($(*)_spec) $(@F).$($(*)_ver) && ln -f -s $(@F).$($(*)_ver) $(@F)

$(dependd)/%.d: src/%.c
	gcc $(arch_cflags) $(defines) $(includes) $($(notdir $*)_includes) $($(notdir $*)_defines) -MM $< -MT $(objd)/$(*).o -MF $@

$(dependd)/%.d: src/bid/%.c
	gcc $(arch_cflags) $(defines) $(includes) $($(notdir $*)_includes) $($(notdir $*)_defines) -MM $< -MT $(objd)/$(*).o -MF $@

$(dependd)/%.fpic.d: src/%.c
	gcc $(arch_cflags) $(defines) $(includes) $($(notdir $*)_includes) $($(notdir $*)_defines) -MM $< -MT $(objd)/$(*).fpic.o -MF $@

$(dependd)/%.fpic.d: src/bid/%.c
	gcc $(arch_cflags) $(defines) $(includes) $($(notdir $*)_includes) $($(notdir $*)_defines) -MM $< -MT $(objd)/$(*).fpic.o -MF $@

