using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace emlextractor
{
    class Program
    {
        static void Main(string[] args)
        {
            var mailReader = new MsgReader.Reader();
            Console.WriteLine("Which folder path to process?");
            var processThisFolder = Console.ReadLine();

            // Prepare the output CSV
            var outputCsv = new List<string>();

            foreach (var f in Directory.GetFiles(processThisFolder, "*.eml", SearchOption.AllDirectories))
            {
                var destination = f + "_eml";
                PrepareDirectory(destination);

                mailReader.ExtractToFolder(f, destination);
                Console.WriteLine("Processing: " + f);

                foreach (var zip in Directory.GetFiles(destination, "*.zip"))
                {
                    var destination2 = zip + "_extracted";

                    // Extract it to a fresh directory
                    PrepareDirectory(destination2);

                    ZipFile.ExtractToDirectory(zip, destination2);

                    // Check the files inside the ZIP
                    foreach (var csv in Directory.GetFiles(destination2, "*.csv"))
                    {
                        var filename = Path.GetFileNameWithoutExtension(csv);
                        if (!filename.Contains("EPM") && !filename.Contains("Error"))
                        {
                            Console.WriteLine("* CSV FOUND!, appending...");

                            var tmp = File.ReadAllLines(csv);
                            outputCsv.Add(tmp[1]);
                        }
                    }
                }
            }

            File.WriteAllLines(Path.Combine(processThisFolder, "output_combined.csv"), outputCsv);
        }

        private static void PrepareDirectory(string d)
        {
            if (Directory.Exists(d))
                Directory.Delete(d, true);

            Directory.CreateDirectory(d);
        }
    }
}
