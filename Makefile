PYTHON ?= python


SCENE_NAMES = LongCharView RcProbeNear RcProbeFar ProbeGrid InterpolatedProbe PenumbraCriterion
JSON_SCENES := $(SCENE_NAMES:%=slides/%.json)
HTML_SCENES := $(SCENE_NAMES:%=intermediate_html/%.html)
GENERATED_ASSETS :=$(SCENE_NAMES:%=generated/%_assets)

slides/%.json: %.py RadianceIntervals.py manim.cfg
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

dist: presentation.html
	mkdir -p dist
	cp presentation.html dist/index.html
	cp -r generated dist
	cp -r static_assets dist
	cp -r presentation_temp_files dist

webp_dist: presentation.html
	mkdir -p webp_dist
	cp presentation.html webp_dist/index.html
	sed -i 's/.png/.webp/g' webp_dist/index.html
	cp -r generated webp_dist
	cp -r presentation_temp_files webp_dist
	cp -r static_assets webp_dist
	cd webp_dist/static_assets; bash ./convert_png_webp.sh; rm *.png

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
	rm -rf dist
	rm -rf webp_dist