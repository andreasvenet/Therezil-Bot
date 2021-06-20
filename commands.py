import eightball
import imagetext
import sad as sad_command
import inspire
import responding

command_prefix = "$"
eightball = eightball.Eightball("8ball")
imagetext = imagetext.Imagetext(command_prefix + "img")
sad = sad_command.Sad("sad")
sad_add = sad_command.Sad(command_prefix + "new")
sad_del = sad_command.Sad(command_prefix + "del")
inspire = inspire.Inspire(command_prefix + "inspire")
responding = responding.Responding(command_prefix + "responding")