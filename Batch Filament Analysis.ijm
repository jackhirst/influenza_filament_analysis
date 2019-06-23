/*
 * Macro template to process multiple images in a folder
 */

#@ File (label = "Input directory", style = "directory") input
output = input
//#@ File (label = "Output directory", style = "directory") output
#@ String (label = "File suffix", value = ".czi") suffix

// See also Process_Folder.py for a version of this code
// in the Python scripting language.

processFolder(input);

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	//list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			processFolder(input + File.separator + list[i]);
		if(endsWith(list[i], suffix))
			processFile(input, list[i]);
	}
}

function processFile(input, file) {
	print("Processing: " + input + File.separator + file);
	open(input + File.separator + file);
	setAutoThreshold("Default dark");
	run("Convert to Mask");
	run("Colors...", "foreground=black background=black selection=yellow");
	run("Particle Remover", "  circularity=0.50-1.00 include");
	//This line depends on which computer I use, have not pinned down the problem yet
	//run("Invert LUT");
	run("Set Scale...", "distance=4.6267 known=0.45 pixel=1 unit=micron");
	run("Ridge Detection", "line_width=5 high_contrast=230 low_contrast=87 extend_line displayresults method_for_overlap_resolution=NONE sigma=2 lower_threshold=3.06 upper_threshold=7.99 minimum_line_length=15 maximum=0");
	selectWindow("Summary");
	saveAs("Results", input + File.separator + getCleanTitle(file) + ".csv");
	run("Close");
	run("Close All");
	close("Results");
	close("Junctions");
}

function getCleanTitle(aString)
{
	last = lastIndexOf(aString, ".");
	cleanTitle = substring(aString, 0, last);
	return cleanTitle;
}
