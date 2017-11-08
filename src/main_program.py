import sys, argparse, heightfield, os, povray_writer, load_info, read_lidar

def render(c1, c2, dir_from, angle, result):
	# Find mdts and ortophotos and write heighfields info 

	mdt_list = load_info.find_mdt(c1[0], c1[1], c2[0], c2[1])
	orto_list = load_info.find_orto(c1[0], c1[1], c2[0], c2[1], mdt_list)

	if len(orto_list) <= 10:
		heightfields = povray_writer.write_heightfields(mdt_list, orto_list) # Generate a string which contain the heightfields to pov file.
		spheres = read_lidar.generate_spheres()

		# Generate povray file

		aspectRatio = povray_writer.write_povray_file(c1, c2, dir_from, angle, heightfields, spheres)
		h = 5000
		w = int(h * aspectRatio + 0.5)

		# Rendering using new povray file

		print("Rendering " + result)
		os.system('povray +Irender.pov +O' + result + ' -D +W' + str(w) + ' +H' + str(h))
		#os.system('rm render.pov')
	else:
		print("Error: The zone to render must be smaller (orto_list > 10). Try with other coordinates.")						

def main():
	# Arguments

	parser = argparse.ArgumentParser(description="First version of Pablo's TFG.")

	parser.add_argument("mdt_directory", help="Directory of the MDT files to transform.")
	parser.add_argument("png_directory", help="PNG files transformed destination directory.")
	parser.add_argument("orto_directory", help="Ortophotos files directory.")
	parser.add_argument("dir_from", help="From direction of the view (only N, S, E or W).")
	parser.add_argument("angle", help="Angle of the view (only 45 or 30).")
	#parser.add_argument("result_name", help="Name of the image (jpg) result.")

	parser.add_argument("--max_height", dest="max_height", type=int, default=2200, metavar="MAX_HEIGHT",
		help="Max height transforming MDT files. Higher heights will be considered MAX_HEIGHT " + 
			"(default value = 2200)")

	parser.add_argument("--all", help="Render all available zones.", action="store_true")

	args = parser.parse_args()

	if (args.angle == "30") or (args.angle == "45"):
		if (args.dir_from == 'S') or (args.dir_from == 'N') or (args.dir_from == 'W') or (args.dir_from == 'E'):

			if args.mdt_directory[-1] != "/":
				args.mdt_directory += "/"
			if args.png_directory[-1] != "/":
				args.png_directory += "/"
			if args.orto_directory[-1] != "/":
				args.orto_directory += "/"	

			# Transform to heightfield	

			#for base, dirs, files in os.walk(args.mdt_directory):
			#	for asc_file in files:
			#		heightfield.transform_file_to_heightfield(args.mdt_directory + asc_file, args.png_directory 
			#			+ asc_file[:-4] + ".png", args.max_height)

			# Load info data to file

			#load_info.load_info(args.png_directory, args.orto_directory)

			#offset = 1000
			offset = 0
			minX = 704000 + offset # Incluído de momento a mano (coordenada central mdt - nºcolumnas/2 * tamaño celda)
			maxX = 704400 + 5760 * 5 - offset # Se comprueba en la lista que valores serían los mayores y cuales los menores
			minY = 4652400 + offset # Se suma el offset para que luego los datos concuerden al aplicarle el offset
			maxY = 4671000 + 4000 * 5 - offset

			if args.all:
				os.system('mkdir result_dir')
				dist_x = 8000
				dist_y = 6000 
				
				x1 = minX
				x_number = 0

				while(x1 + dist_x < maxX): # Recorre las X de menor a mayor
					x_number += 1
					
					y1 = maxY
					y_number = 0
					
					while(y1 - dist_y > minY): # Recorre las Y de mayor a menor
						y_number += 1
						render([x1, y1], [x1 + dist_x, y1 - dist_y], args.dir_from, args.angle, 
							"./result_dir/result_" + str(x_number) + "_" + str(y_number) + ".png")
						y1 -= dist_y

					y_number += 1	
					render([x1, y1], [x1 + dist_x, minY], args.dir_from, args.angle, 
						"./result_dir/result_" + str(x_number) + "_" + str(y_number) + ".png") # La última con la segunda coordenada la menor Y
					x1 += dist_x	

				# Recorre para los últimos valores para las X
					
				x_number += 1

				y1 = maxY
				y_number = 0

				while(y1 - dist_y > minY):
					y_number += 1
					render([x1, y1], [maxX, y1 - dist_y], args.dir_from, args.angle, 
						"./result_dir/result_" + str(x_number) + "_" + str(y_number) + ".png")
					y1 -= dist_y

				y_number += 1	
				render([x1, y1], [maxX, minY], args.dir_from, args.angle, 
					"./result_dir/result_" + str(x_number) + "_" + str(y_number) + ".png")
			else:
				# Ask for coordinates

				coordinates = input("Introduce UTM X and Y coordinates, separated by a blank space and respecting the values min " 
					+ "and max for the coordinates, for upper left vertex (" + str(minX) + " <= X1 <= " + str(maxX) + " " + str(minY) 
					+ " <= Y1 <= " + str(maxY) + "): ")
				coordinates1 = coordinates.split()
				coordinates1 = ["711500", "4670000"]

				if (len(coordinates1) == 2 and float(coordinates1[0]) >= minX and float(coordinates1[0]) <= maxX and 
						float(coordinates1[1]) >= minY and float(coordinates1[1]) <= maxY):
					
					coordinates = input("Introduce UTM X and Y coordinates, separated by a blank space and respecting the values min " 
						+ "and max for the coordinates, for bottom right vertex (" + coordinates1[0] + " <= X2 <= " + str(maxX) + " " + str(minY) 
						+ " <= Y2 <= " + coordinates1[1] + "): ")
					coordinates2 = coordinates.split()
					coordinates2 = ["715000", "4667000"]

					if (len(coordinates2) == 2 and float(coordinates2[0]) >= minX and float(coordinates2[0]) <= maxX and 
							float(coordinates2[1]) >= minY and float(coordinates2[1]) <= maxY and coordinates1[0] < coordinates2[0]
							and coordinates1[1] > coordinates2[1]):
						
						# Offset to adjust later during join process

						coordinates1[0] = float(coordinates1[0]) - offset
						coordinates2[0] = float(coordinates2[0]) + offset
						coordinates1[1] = float(coordinates1[1]) + offset
						coordinates2[1] = float(coordinates2[1]) - offset

						render(coordinates1, coordinates2, args.dir_from, args.angle, "./result.png")	
					else:
						print("Error: Introduce UTM coordinates correctly.")
				else:
					print("Error: Introduce UTM coordinates correctly.")				
		else:	
			print("ERROR: dir_from must be N, S, W or E.")
	else:
		print("ERROR: angle must be 45 or 30.")	

if __name__ == "__main__":
    main()