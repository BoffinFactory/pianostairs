# Generates the various sound files.
# Requires timidity and lilypond to be installed and in the $PATH.
# I'm not including sounds/* in the git repo, since it's large, but we'll want
# to generate them all on a machine with a good midi setup and then copy them
# to the Pi instead of generating them there, probably.

SHELL=/bin/bash
.SECONDARY:

#These are the only two variables that should be modified
SOUNDS_DIR=sounds
INSTRUMENTS := \
	piano:acoustic_grand \
	guitar:acoustic_guitar_(nylon) \
	cello:cello \
	timpani:timpani \
	saxophone:baritone_sax \
	bassoon:bassoon \

TONES := C Db D Eb E F Gb G Ab A Bb B
OCTAVES := $(shell seq 0 8)

# Usage: $(call add-tone instrument tone octave)
# Sets up all the necessary target-specific variables for this specific note
# and registers the note as a dependency of the instrument
define add-tone

$(1): $(SOUNDS_DIR)/$(1)-$(2)$(3).wav
$(SOUNDS_DIR)/$(1)-$(2)$(3).wav: tone=$(2)
$(SOUNDS_DIR)/$(1)-$(2)$(3).wav: octave=$(3)
endef

# Usage: add-instrument instrument
# Sets target-specific variables for that instrument, makes all the add-tone calls for that instrument,
# and adds the instrument to all's dependency list
define add-instrument

$(eval instrument=$(word 1,$(subst :, ,$(1))))
$(eval midi=$(subst _, ,$(word 2,$(subst :, ,$(1)))))

instruments += $(instrument)
all: $(instrument)
$(instrument): midi_instrument="$(midi)"

$(foreach tone,$(TONES),$(foreach octave,$(OCTAVES),$(call add-tone,$(instrument),$(tone),$(octave))))
endef

# Needs to appear before the eval, to make it the default
all:

# Generates all the dependencies
$(eval $(foreach i,$(INSTRUMENTS),$(call add-instrument,$i)))


.PHONY: all clean init $(instruments)
all: $(instruments)

init:
	@which timidity > /dev/null || (echo "ERROR: Install timidity package"; false)
	@which lilypond > /dev/null || (echo "ERROR: Install lilypond package"; false)
	@mkdir -p $(SOUNDS_DIR)

clean:
	rm $(SOUNDS_DIR)/*.wav

%.wav: %.midi
	timidity -idq "$<" -Ow

%.midi: %.ly
	lilypond -so "$(basename $@)" "$<"
	
%.ly: init
	$(info generating $@)
	@{ \
	echo '\version "2.16.2"'; \
	echo '\score {'; \
	echo '\new PianoStaff'; \
	echo '\relative $(tone),,, {' | sed 's/b/es/g' | tr '[A-Z]' '[a-z]'; \
	echo '\set Staff.midiInstrument = #$(midi_instrument)'; \
	echo -n '$(tone)' | sed 's/b/es/g' | tr '[A-Z]' '[a-z]'; \
	for i in `seq 1 $(octave)`; do echo -n "'"; done; \
	echo '2'; \
	echo '}'; \
	echo '\midi { }'; \
	echo '}'; \
	} > "$@"


