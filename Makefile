PYTHON ?= python


SCENE_NAMES = LongCharView RcProbeNear RcProbeFar
HTML_SCENES := $(SCENE_NAMES:%=intermediate_html/%.html)

slides/%.json: %.py
	$(PYTHON) -m manim_slides render  $< $*

intermediate_html/%.html: slides/%.json
	$(PYTHON) -m manim_slides convert $* $@ -cdata_uri=true

presentation.html: BuildSlides.py $(HTML_SCENES)
	$(PYTHON) $< $(SCENE_NAMES)

.PHONY: clean
clean:
	rm -rf intermediate_html
	rm -rf presentation.html

.PHONY: allclean
allclean: clean
	rm -rf slides
	rm -rf media