PYTHON ?= python


SCENE_NAMES = LongCharView RcProbeNear RcProbeFar ProbeGrid InterpolatedProbe PenumbraCriterion
JSON_SCENES := $(SCENE_NAMES:%=slides/%.json)
HTML_SCENES := $(SCENE_NAMES:%=intermediate_html/%.html)
GENERATED_ASSETS :=$(SCENE_NAMES:%=generated/%_assets)

slides/%.json: %.py RadianceIntervals.py
	$(PYTHON) -m manim_slides render -qk $< $*

# -cdata_uri=true
intermediate_html/%.html: slides/%.json
	$(PYTHON) -m manim_slides convert $* $@

generated/%_assets: intermediate_html/%.html
	mkdir -p generated
	cp -r intermediate_html/$*_assets generated

presentation.html: presentation_temp.qmd my_style.scss
	quarto render $< -o $@

presentation_temp.qmd: BuildSlides.py presentation.qmd $(GENERATED_ASSETS)
	$(PYTHON) $< $(SCENE_NAMES)

# Preserve the intermediate outputs
all_slides: $(JSON_SCENES)
all_html: $(HTML_SCENES)

.PHONY: clean
clean:
	rm -rf intermediate_html
	rm -rf presentation.html
	rm -rf generated

.PHONY: allclean
allclean: clean
	rm -rf slides
	rm -rf media