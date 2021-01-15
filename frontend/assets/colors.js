// https://coolors.co/f94144-f65a38-f3722c-f8961e-f9c74f-c5c35e-90be6d-43aa8b-4d908e-577590
/* Extended Array */
const COLORS = [
  { name: 'Queen Blue', hex: '#577590', rgb: [87, 117, 144], cmyk: [40, 19, 0, 44], hsb: [208, 40, 56], hsl: [208, 25, 45], lab: [48, -4, -18] },
  { name: 'Zomp', hex: '#43aa8b', rgb: [67, 170, 139], cmyk: [61, 0, 18, 33], hsb: [162, 61, 67], hsl: [162, 43, 46], lab: [63, -37, 7] },
  { name: 'Dark Khaki', hex: '#c5c35e', rgb: [197, 195, 94], cmyk: [0, 1, 52, 23], hsb: [59, 52, 77], hsl: [59, 47, 57], lab: [77, -13, 50] },
  { name: 'Yellow Orange Color Wheel', hex: '#f8961e', rgb: [248, 150, 30], cmyk: [0, 40, 88, 3], hsb: [33, 88, 97], hsl: [33, 94, 55], lab: [71, 29, 71] },
  { name: 'Red Salsa', hex: '#f94144', rgb: [249, 65, 68], cmyk: [0, 74, 73, 2], hsb: [359, 74, 98], hsl: [359, 94, 62], lab: [56, 69, 41] },
  { name: 'Cadet Blue', hex: '#4d908e', rgb: [77, 144, 142], cmyk: [47, 0, 1, 44], hsb: [178, 47, 56], hsl: [178, 30, 43], lab: [56, -22, -6] },
  { name: 'Pistachio', hex: '#90be6d', rgb: [144, 190, 109], cmyk: [24, 0, 43, 25], hsb: [94, 43, 75], hsl: [94, 38, 59], lab: [72, -30, 36] },
  { name: 'Maize Crayola', hex: '#f9c74f', rgb: [249, 199, 79], cmyk: [0, 20, 68, 2], hsb: [42, 68, 98], hsl: [42, 93, 64], lab: [83, 6, 64] },
  { name: 'Orange Red', hex: '#f3722c', rgb: [243, 114, 44], cmyk: [0, 53, 82, 5], hsb: [21, 82, 95], hsl: [21, 89, 56], lab: [63, 46, 59] }
]

class ColorGetter {
    currentIndex = -1
    numTotalLoops= -1

    _increment () {
      this.currentIndex = (this.currentIndex + 1) % COLORS.length
      if (this.currentIndex % COLORS.length === 0) {
        this.numTotalLoops += 1
      }
    }

    getNextColor () {
      this._increment()
      return COLORS[this.currentIndex].hex // TODO: increase saturation
    }

    getNextColors (numColors) {
      return Array.from({ length: numColors }, () => this.getNextColor())
    }
}

export { ColorGetter }
