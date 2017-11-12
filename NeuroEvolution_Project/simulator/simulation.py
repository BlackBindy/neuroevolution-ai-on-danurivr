class Simulation:
	def __init__(self, total_frames, fps=60):
		self.total_frames = total_frames
		self.fps = fps

		# private
		self.__frame_count = 1

	def get_frame_count(self):
		return self.__frame_count

	def inc_frame_count(self):
		self.__frame_count += 1