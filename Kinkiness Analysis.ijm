/*
 * Macro template to process multiple images in a folder
 */

#@ File (label = "Input directory", style = "directory") input
#@ File (label = "Output directory", style = "directory") output
#@ String (label = "File suffix", value = ".czi") suffix
#@ String (label = "Experiment Code", value = ".czi") exptCode

run("Set Measurements...", "area fit redirect=None decimal=2");
processFolder(input);

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input)
{
	list = getFileList(input);
	//list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
		{
			processFolder(input + File.separator + list[i]);
		}
		if(endsWith(list[i], suffix))
		{
			processFile(input, list[i]);
		}
		if(i == list.length-1)
			{
			print("I think I finished a folder");
			currentLocation = input + File.separator + list[i];
			title = getFolderTitle(currentLocation);
			// TODO work out how I want these organised when I'm finished, and how to get them in a useful folder
			print("Saving as " + output + File.separator + exptCode + " " + title + ".csv");
			saveAs("Results", output + File.separator + exptCode + " " + title + ".csv");
			close("Results");
			}
	}
}

function processFile(input, file) {
	print("Processing: " + input + File.separator + file);
	open(input + File.separator + file);
	setAutoThreshold("Default dark");
	run("Convert to Mask");
	run("Analyze Particles...", "  circularity=0.00-0.50 display include");
	//run("Invert LUT");
	//run("Particle Remover", "  circularity=0.50-1.00 include");
	run("Close All");
	//selectWindow("Summary");
	//saveAs("Results", input + File.separator + getCleanTitle(file) + "kinks" + ".csv");
}

function getCleanTitle(aString)
{
	last = lastIndexOf(aString, ".");
	cleanTitle = substring(aString, 0, last);
	return cleanTitle;
}



function getFolderTitle(aString)
{
	last = lastIndexOf(aString, File.separator);
	newString = substring(aString, 0, last);
	penultimate = lastIndexOf(newString, File.separator);
	folderTitle = substring(aString, penultimate + 1, last - 1);
	return folderTitle;
}
