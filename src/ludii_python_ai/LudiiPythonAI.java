package ludii_python_ai;

import java.io.File;
import java.net.URL;
import java.util.concurrent.ThreadLocalRandom;
import java.util.regex.Pattern;

import org.jpy.PyLib;
import org.jpy.PyModule;
import org.jpy.PyObject;

import game.Game;
import main.collections.FastArrayList;
import util.AI;
import util.Context;
import util.Move;
import utils.AIUtils;

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
		FastArrayList<Move> legalMoves = game.moves(context).moves();
		
		// If we're playing a simultaneous-move game, some of the legal moves may be 
		// for different players. Extract only the ones that we can choose.
		if (!game.isAlternatingMoveGame())
			legalMoves = AIUtils.extractMovesForMover(legalMoves, player);
		
		final int r = ThreadLocalRandom.current().nextInt(legalMoves.size());
		return legalMoves.get(r);
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
		
		// Get the UCT class from Python
		final PyObject pythonUctClass = ludiiPythonModule.getAttribute("UCT");
		
		// Instantiate a new AI (implemented in Python)
		pythonAI = ludiiPythonModule.call("UCT");
	}
	
	//-------------------------------------------------------------------------

}
