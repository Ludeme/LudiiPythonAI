package ludii_python_ai;

import java.io.File;
import java.net.URL;
import java.util.regex.Pattern;

import org.jpy.PyLib;
import org.jpy.PyModule;
import org.jpy.PyObject;

import game.Game;
import util.AI;
import util.Context;
import util.Move;

/**
 * Example Java wrapper for a Ludii AI implemented in Python
 *
 * @author Dennis Soemers
 */
public class LudiiPythonAI extends AI
{
	
	//-------------------------------------------------------------------------
	
	/** Our player index */
	protected int player = -1;
	
	/** The "ludii_python.uct" Python Module */
	private PyModule ludiiPythonModule = null;
	
	/** This will hold our AI object (implemented in Python) */
	private PyObject pythonAI = null;
	
	/** Did we perform initialisation required for JPY? */
	private boolean initialisedJpy = false;
	
	//-------------------------------------------------------------------------
	
	/**
	 * Constructor
	 */
	public LudiiPythonAI()
	{
		this.friendlyName = "Example Ludii Python AI";
	}
	
	//-------------------------------------------------------------------------

	@Override
	public Move selectAction
	(
		final Game game, 
		final Context context, 
		final double maxSeconds,
		final int maxIterations,
		final int maxDepth
	)
	{
		return (Move) pythonAI.call
		(
			"select_action", game, context, 
			Double.valueOf(maxSeconds), 
			Integer.valueOf(maxIterations), 
			Integer.valueOf(maxDepth)
		).getObjectValue();
	}
	
	@Override
	public void initAI(final Game game, final int playerID)
	{
		this.player = playerID;
		
		if (!initialisedJpy)
		{
			// We always expect this AI class to be in a JAR file. Let's find out where our JAR file is
			final URL jarLoc = LudiiPythonAI.class.getProtectionDomain().getCodeSource().getLocation();
			final String jarPath = 
					new File(jarLoc.getFile()).getParent()
					.replaceAll(Pattern.quote("\\"), "/")
					.replaceAll(Pattern.quote("file:"), "");
			
			// Set JPY config property relative to this JAR path
			System.setProperty("jpy.config", jarPath + "/libs/jpyconfig.properties");

			// Make sure that Python is running
			if (!PyLib.isPythonRunning()) 
			{
				// We expect the python code to be in the same directory as this JAR file;
				// therefore, we include this path such that Python can discover our python code
				PyLib.startPython(jarPath);
			}
			
			ludiiPythonModule = PyModule.importModule("ludii_python.uct");
			initialisedJpy = true;
		}		
		
		// Instantiate a new AI (implemented in the Python class "UCT")
		pythonAI = ludiiPythonModule.call("UCT");
		
		pythonAI.call("init_ai", game, Integer.valueOf(playerID));
	}
	
	//-------------------------------------------------------------------------

}
