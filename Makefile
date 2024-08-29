PYTHON ?= python


SCENE_NAMES = LongCharView RcProbeNear RcProbeFar ProbeGrid InterpolatedProbe PenumbraCriterion
JSON_SCENES := $(SCENE_NAMES:%=slides/%.json)
HTML_SCENES := $(SCENE_NAMES:%=intermediate_html/%.html)

slides/%.json: %.py RadianceIntervals.py
	$(PYTHON) -m manim_slides render  $< $*

intermediate_html/%.html: slides/%.json
	$(PYTHON) -m manim_slides convert $* $@ -cdata_uri=true

presentation.html: BuildSlides.py presentation_template.j2 $(HTML_SCENES)
	$(PYTHON) $< $(SCENE_NAMES)

# Preserve the intermediate outputs
all_slides: $(JSON_SCENES)

.PHONY: clean
clean:
	rm -rf intermediate_html
	rm -rf presentation.html

.PHONY: allclean
allclean: clean
	rm -rf slides
	rm -rf media