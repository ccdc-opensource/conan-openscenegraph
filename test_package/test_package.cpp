#include <osg/ArgumentParser>
#include <FreeTypeLibrary.h>

int main( int argc, char** argv )
{
    osg::ArgumentParser arguments(&argc,argv);

    arguments.getApplicationUsage()->setDescription(arguments.getApplicationName()+" is the example which runs units tests.");
    arguments.getApplicationUsage()->setCommandLineUsage(arguments.getApplicationName()+" [options]");
    arguments.getApplicationUsage()->addCommandLineOption("-h or --help","Display this information");
	
    FreeTypeLibrary* ftl = FreeTypeLibrary::instance();
    if (!ftl)
        return 1;
	return 0;
}