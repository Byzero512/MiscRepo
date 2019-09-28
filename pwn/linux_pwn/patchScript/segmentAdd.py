import lief
# attention: dont use on i386-non-pie
def segmentAdd(path):
    binary = lief.parse(path)
    segment = lief.ELF.Segment()
    segment.type = lief.ELF.SEGMENT_TYPES.LOAD
    segment.content = [0x90, 0x90, 0x90, 0x90]
    segment.add(lief.ELF.SEGMENT_FLAGS.R)
    segment.add(lief.ELF.SEGMENT_FLAGS.X)
    segment.add(lief.ELF.SEGMENT_FLAGS.W)
    segment.alignment=0x1000
    binary.add(segment)
    binary.write('hello_lief')
