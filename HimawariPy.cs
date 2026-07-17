using System.Diagnostics;
using System.IO;

class Program {
    static void Main(string[] args) {
        ProcessStartInfo startInfo = new ProcessStartInfo();
        startInfo.FileName = "pythonw.exe";
        startInfo.Arguments = "-m himawaripy";
        startInfo.WindowStyle = ProcessWindowStyle.Hidden;
        startInfo.CreateNoWindow = true;
        startInfo.UseShellExecute = true;
        
        try {
            Process.Start(startInfo);
        } catch (System.Exception) {
            // If pythonw.exe is not in PATH, try finding it via python command
            try {
                startInfo.FileName = "python.exe";
                Process.Start(startInfo);
            } catch (System.Exception) {
                // Ignore failure
            }
        }
    }
}
