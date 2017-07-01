import xmlschema
from buildingsync.models import Schema, BuildingSyncAttribute

SCHEMA_NAME = "BuildingSync, Version 2.0.0"
SCHEMA_VERSION = 2


class BuildingSyncSchemaElement(object):

    def __init__(self):
        pass


class BuildingSyncSchemaRoot(BuildingSyncSchemaElement):
    def __init__(self):
        super(BuildingSyncSchemaRoot, self).__init__()
        self.named_elements = []
        self.ref_elements = []
        self.complex_types = []
        self.simple_types = []
        self.attributes = []


class ReferenceElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(ReferenceElement, self).__init__()
        self.attributes = []
        self.annotations = []
        self.ref_type = None


class NamedElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(NamedElement, self).__init__()
        self.annotations = []
        self.complex_types = []
        self.simple_types = []
        self.name = ""
        self.type = None


class AnnotationElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(AnnotationElement, self).__init__()
        self.documentation = ""


class AttributeElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(AttributeElement, self).__init__()
        self.simple_types = []
        self.annotations = []


class ComplexTypeElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(ComplexTypeElement, self).__init__()
        self.sequences = []
        self.simple_contents = []
        self.attributes = []
        self.choices = []


class SequenceElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(SequenceElement, self).__init__()
        self.named_elements = []
        self.ref_elements = []


class SimpleContentElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(SimpleContentElement, self).__init__()
        self.extensions = []


class ExtensionElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(ExtensionElement, self).__init__()
        self.attributes = []


class SimpleTypeElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(SimpleTypeElement, self).__init__()
        self.restrictions = []


class RestrictionElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(RestrictionElement, self).__init__()
        self.enumerations = []


class ChoiceElement(BuildingSyncSchemaElement):
    def __init__(self):
        super(ChoiceElement, self).__init__()
        self.named_elements = []
        self.ref_elements = []


class BuildingSyncSchemaProcessor(object):

    def __init__(self, xml_schema_instance):
        """
        Creates a new BuildingSync schema processor.  The schema has already been *parsed* by the XMLSchema library.
        This class manages processing the complex data structure into a state targeted for BuildingSync schema specifics
        :param xml_schema_instance: An xmlschema.XMLSchema instance ready to process
        """
        self.xml_schema_structure = xml_schema_instance
        self.type_definitions = []
        self.all_named_elements = []
        self.type_references = []
        self.named_complex_types = {}
        self.full_schema = self._read_schema(self.xml_schema_structure.root)
        self.check_all_type_references()

    def check_all_type_references(self):
        for type_ref in self.type_references:
            looking_for_type_name = type_ref.ref_type.split(':')[1]  # it starts with the namespace 'auc:'
            found = False
            for ne in self.all_named_elements:
                if looking_for_type_name == ne.name:
                    found = True
                    break
            if found:
                continue
            raise Exception("Couldn't find reference %s" % looking_for_type_name)
        print("All type refs were properly accounted.")

    def _read_schema(self, root_element):
        full_schema = BuildingSyncSchemaRoot()
        for child in root_element.getchildren():
            if child.tag.endswith('element'):
                if 'name' in child.attrib:
                    full_schema.named_elements.append(self._read_named_element(child))
                elif 'ref' in child.attrib:
                    full_schema.ref_elements.append(self._read_ref_element(child))
                else:
                    raise Exception("Invalid element type in _read_schema, no name or ref in attrib...")
            elif child.tag.endswith('complexType'):
                full_schema.complex_types.append(self._read_complex_type(child))
            elif child.tag.endswith('simpleType'):
                full_schema.simple_types.append(self._read_simple_type(child))
            elif child.tag.endswith('attribute'):
                full_schema.attributes.append(self._read_attribute(child))
            else:
                raise Exception("Invalid tag type in _read_schema: " + child.tag)
        return full_schema

    def _read_ref_element(self, parent_object):
        ref_element = ReferenceElement()
        ref_element.ref_type = parent_object.attrib['ref']
        for child in parent_object.getchildren():
            if child.tag.endswith('attribute'):
                ref_element.attributes.append(self._read_attribute(child))
            elif child.tag.endswith('annotation'):
                ref_element.annotations.append(self._read_annotation(child))
            else:
                raise Exception("Invalid tag type in _read_ref_element: " + child.tag)
        self.type_references.append(ref_element)
        return ref_element

    def _read_named_element(self, parent_object):
        named_element = NamedElement()
        named_element.name = parent_object.attrib['name']
        if 'type' in parent_object.attrib:
            named_element.type = parent_object.attrib['type']
        for child in parent_object.getchildren():
            if child.tag.endswith('annotation'):
                named_element.annotations.append(self._read_annotation(child))
            elif child.tag.endswith('complexType'):
                named_element.complex_types.append(self._read_complex_type(child))
            elif child.tag.endswith('simpleType'):
                named_element.simple_types.append(self._read_simple_type(child))
            else:
                raise Exception("Invalid tag type in _read_named_element: " + child.tag)
        if named_element.type:
            self.type_definitions.append(named_element)
        self.all_named_elements.append(named_element)
        return named_element

    def _read_annotation(self, parent_object):
        annotation = AnnotationElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('documentation'):
                annotation.documentation = child.text
            else:
                raise Exception("Invalid tag type in _read_annotation: " + child.tag)
        return annotation

    def _read_attribute(self, parent_object):
        attribute = AttributeElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('simpleType'):
                attribute.simple_types.append(self._read_simple_type(child))
            elif child.tag.endswith('annotation'):
                attribute.annotations.append(self._read_annotation(child))
            else:
                raise Exception("Invalid tag type in _read_attribute: " + child.tag)
        return attribute

    def _read_complex_type(self, parent_object):
        this_complex_type = ComplexTypeElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('sequence'):
                this_complex_type.sequences.append(self._read_sequence(child))
            elif child.tag.endswith('simpleContent'):
                this_complex_type.simple_contents.append(self._read_simple_content(child))
            elif child.tag.endswith('attribute'):
                this_complex_type.attributes.append(self._read_attribute(child))
            elif child.tag.endswith('choice'):
                this_complex_type.choices.append(self._read_choice(child))
            else:
                raise Exception("Invalid tag type in _read_complex_type: " + child.tag)
        if 'name' in parent_object.attrib:
            self.named_complex_types[parent_object.attrib['name']] = this_complex_type
        return this_complex_type

    def _read_sequence(self, parent_object):
        this_sequence = SequenceElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('element'):
                if 'name' in child.attrib:
                    this_sequence.named_elements.append(self._read_named_element(child))
                elif 'ref' in child.attrib:
                    this_sequence.ref_elements.append(self._read_ref_element(child))
                else:
                    raise Exception("Invalid element type in _read_sequence, no name or ref in attrib...")
            else:
                raise Exception("Invalid tag type in _read_sequence: " + child.tag)
        return this_sequence

    def _read_simple_content(self, parent_object):
        this_simple_content = SimpleContentElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('extension'):
                this_simple_content.extensions.append(self._read_extension(child))
            else:
                raise Exception("Invalid tag type in _read_simple_content: " + child.tag)
        return this_simple_content

    def _read_extension(self, parent_object):
        this_extension = ExtensionElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('attribute'):
                this_extension.attributes.append(self._read_attribute(child))
            else:
                raise Exception("Invalid tag type in _read_extension: " + child.tag)
        return this_extension

    def _read_simple_type(self, parent_object):
        this_simple_content = SimpleTypeElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('restriction'):
                this_simple_content.restrictions.append(self._read_restriction(child))
            else:
                raise Exception("Invalid tag type in _read_simple_type: " + child.tag)
        return this_simple_content

    def _read_restriction(self, parent_object):
        this_restriction = RestrictionElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('enumeration'):
                this_restriction.enumerations.append(child.attrib['value'])
            else:
                raise Exception("Invalid tag type in _read_restriction: " + child.tag)
        return this_restriction

    def _read_choice(self, parent_object):
        this_choice = ChoiceElement()
        for child in parent_object.getchildren():
            if child.tag.endswith('element'):
                if 'name' in child.attrib:
                    this_choice.named_elements.append(self._read_named_element(child))
                elif 'ref' in child.attrib:
                    this_choice.ref_elements.append(self._read_ref_element(child))
                else:
                    raise Exception("Invalid element type in _read_schema, no name or ref in attrib...")
            else:
                raise Exception("Invalid tag type in _read_choice: " + child.tag)
        return this_choice

    def generate_data_rows(self):
        _, full_schema_rows = self.walk_single_element(self.full_schema, "root", 1, 0)
        return full_schema_rows

    def walk_single_element(self, parent_element, root_path, current_tree_level, current_index):
        return_rows = []
        num_added = 0
        if type(parent_element) is BuildingSyncSchemaRoot:
            for elem in parent_element.named_elements:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'NAMED: ' + elem.name, 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.ref_elements:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'REF: ' + elem.ref_type, 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.complex_types:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'COMPLEXTYPE', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is NamedElement:
            for elem in parent_element.annotations:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'ANNOTATION', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.complex_types:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'COMPLEXTYPE', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.simple_types:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'SIMPLETYPE', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is ReferenceElement:
            for elem in parent_element.annotations:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'ANNOTATION', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.attributes:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'ATTRIBUTE', 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level+1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is ComplexTypeElement:
            for elem in parent_element.sequences:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'SEQUENCE', 'path': 'SOMETHING', '$$treeLevel': current_tree_level,
                                    'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level + 1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is SequenceElement:
            for elem in parent_element.named_elements:
                current_index += 1
                num_added += 1
                if elem.type:
                    return_rows.append({'name': 'NAMED/TYPED: ' + elem.name + '/' + elem.type, 'path': 'SOMETHING',
                                        '$$treeLevel': current_tree_level, 'index': current_index})
                else:
                    return_rows.append(
                        {'name': 'NAMED: ' + elem.name, 'path': 'SOMETHING', '$$treeLevel': current_tree_level,
                         'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level + 1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            for elem in parent_element.ref_elements:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'REF: ' + elem.ref_type, 'path': 'SOMETHING', '$$treeLevel': current_tree_level,
                                    'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level + 1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is AnnotationElement:
            current_index += 1
            num_added += 1
            if parent_element.documentation:
                if len(parent_element.documentation) > 40:
                    doc_to_show = parent_element.documentation[:37] + '...'
                else:
                    doc_to_show = parent_element.documentation
            else:
                doc_to_show = "**no documentation element**"
            return_rows.append({'name': 'ANNOTATION: Doc=\"%s\"' % doc_to_show, 'path': 'SOMETHING', '$$treeLevel': current_tree_level, 'index': current_index})
            return num_added, return_rows
        elif type(parent_element) is SimpleTypeElement:
            for elem in parent_element.restrictions:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'RESTRICTION', 'path': 'SOMETHING', '$$treeLevel': current_tree_level,
                                    'index': current_index})
                this_num_added, new_rows = self.walk_single_element(elem, "", current_tree_level + 1, current_index)
                current_index += this_num_added
                num_added += this_num_added
                return_rows.extend(new_rows)
            return num_added, return_rows
        elif type(parent_element) is RestrictionElement:
            for elem in parent_element.enumerations:
                current_index += 1
                num_added += 1
                return_rows.append({'name': 'Enumeration: ' + elem, 'path': 'SOMETHING', '$$treeLevel': current_tree_level,
                                    'index': current_index})
            return num_added, return_rows
        else:
            raise Exception("Need to implement walking for type: " + str(type(parent_element)))
        # for child in parent_element:
        #     if 'name' in child.attrib:
        #         this_child_name = child.attrib['name']
        #         this_child_type = 'type_unknown'
        #         if 'type' in child.attrib:
        #             this_child_type = child.attrib['type']
        #         this_child_path = root_path + "." + this_child_name
        #         schema_entries.append({'$$treeLevel': current_tree_level, 'name': this_child_name, 'index': current_index,
        #                                'path': this_child_path + ' {' + this_child_type + '}', 'type': this_child_type})
        #     else:
        #         this_child_path = root_path  # then we have some weird list/sequence/something
        #     get_node(child, this_child_path, current_tree_level + 1)


def reset_schema():

    # Delete any previous schemas (and attributes??)
    Schema.objects.all().delete()
    BuildingSyncAttribute.objects.all().delete()

    # Create a schema to work with
    s = Schema(name=SCHEMA_NAME, version=SCHEMA_VERSION)
    s.save()

    # parse the schema itself to get all entries
    my_schema = xmlschema.XMLSchema('buildingsync/schemas/BuildingSync_2_0.xsd')
    # root_element = my_schema.root
    # get_node(root_element, "root", 1)

    bs_processor = BuildingSyncSchemaProcessor(my_schema)
    schema_entries = bs_processor.generate_data_rows()

    # Create database entries for each schema entry
    for se in schema_entries:
        b = BuildingSyncAttribute(name=se['path'], tree_level=se['$$treeLevel'], index=se['index'], schema=s)
        b.save()

    # Return the schema
    return s
